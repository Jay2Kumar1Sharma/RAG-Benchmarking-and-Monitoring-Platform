import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any

import httpx

from app.core.exceptions import AppError
from app.models.rag import GenerationResult, TextChunk
from app.observability.metrics import GENERATION_LATENCY, TOKEN_USAGE


class LLMProvider(ABC):
    provider: str

    @abstractmethod
    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        raise NotImplementedError

    async def stream(self, question: str, contexts: list[TextChunk]):
        result = await self.generate(question, contexts)
        for token in result.answer.split():
            yield f"data: {token}\n\n"
            await asyncio.sleep(0)


class MockGroundedLLM(LLMProvider):
    provider = "mock"

    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        start = time.perf_counter()
        cited = []
        for index, chunk in enumerate(contexts[:3], start=1):
            sentence = chunk.text.strip().replace("\n", " ")[:280]
            cited.append(f"[{index}] {sentence}")
        if cited:
            answer = f"Based on the retrieved enterprise context: {' '.join(cited)}"
        else:
            answer = "I do not have enough retrieved context to answer this safely."
        prompt_tokens = sum(len(chunk.text.split()) for chunk in contexts) + len(question.split())
        completion_tokens = len(answer.split())
        latency_ms = (time.perf_counter() - start) * 1000
        GENERATION_LATENCY.labels(provider=self.provider).observe(latency_ms / 1000)
        TOKEN_USAGE.labels(provider=self.provider, type="prompt").inc(prompt_tokens)
        TOKEN_USAGE.labels(provider=self.provider, type="completion").inc(completion_tokens)
        return GenerationResult(
            answer,
            confidence=0.72 if contexts else 0.1,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=latency_ms,
        )


class OpenAILLM(LLMProvider):
    provider = "openai"

    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        raise NotImplementedError("OpenAI generation requires OPENAI_API_KEY and provider wiring.")


class GroqLLM(LLMProvider):
    provider = "groq"

    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        raise NotImplementedError("Groq generation requires GROQ_API_KEY and provider wiring.")


class GeminiLLM(LLMProvider):
    provider = "gemini"

    def __init__(self, api_key: str | None, model: str = "gemini-2.5-flash-lite") -> None:
        self.api_key = api_key
        self.model = model

    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        if not self.api_key:
            raise AppError("GEMINI_API_KEY is required when DEFAULT_LLM_PROVIDER=gemini")

        start = time.perf_counter()
        prompt = _grounded_prompt(question, contexts)
        payload = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            "You are a grounded enterprise RAG assistant. Answer only from "
                            "the supplied context and cite supporting sources like [1]."
                        )
                    }
                ]
            },
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "topP": 0.9},
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent"
        )
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, params={"key": self.api_key}, json=payload)
        if response.status_code >= 400:
            raise AppError(f"Gemini generation failed with HTTP {response.status_code}", 502)

        data = response.json()
        answer = _extract_gemini_text(data)
        usage = data.get("usageMetadata", {})
        prompt_tokens = int(usage.get("promptTokenCount", len(prompt.split())))
        completion_tokens = int(usage.get("candidatesTokenCount", len(answer.split())))
        latency_ms = (time.perf_counter() - start) * 1000
        GENERATION_LATENCY.labels(provider=self.provider).observe(latency_ms / 1000)
        TOKEN_USAGE.labels(provider=self.provider, type="prompt").inc(prompt_tokens)
        TOKEN_USAGE.labels(provider=self.provider, type="completion").inc(completion_tokens)
        return GenerationResult(
            answer=answer,
            confidence=0.78 if contexts else 0.25,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=latency_ms,
        )


def estimate_cost_usd(
    prompt_tokens: int,
    completion_tokens: int,
    prompt_rate: float = 0.0,
    completion_rate: float = 0.0,
) -> float:
    return round((prompt_tokens / 1_000_000 * prompt_rate) + (completion_tokens / 1_000_000 * completion_rate), 6)


def _grounded_prompt(question: str, contexts: list[TextChunk]) -> str:
    context_block = "\n\n".join(
        f"[{index}] {chunk.text}" for index, chunk in enumerate(contexts, start=1)
    )
    return (
        "Question:\n"
        f"{question}\n\n"
        "Retrieved context:\n"
        f"{context_block or 'No retrieved context was provided.'}\n\n"
        "Instructions:\n"
        "- Answer only from the retrieved context.\n"
        "- Cite every factual claim with source numbers like [1].\n"
        "- If the context is insufficient, say so."
    )


def _extract_gemini_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates") or []
    if not candidates:
        return "I do not have enough retrieved context to answer this safely."
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(str(part.get("text", "")) for part in parts).strip()
    return text or "I do not have enough retrieved context to answer this safely."
