import asyncio
import time
from abc import ABC, abstractmethod

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

    async def generate(self, question: str, contexts: list[TextChunk]) -> GenerationResult:
        raise NotImplementedError("Gemini generation requires GEMINI_API_KEY and provider wiring.")


def estimate_cost_usd(
    prompt_tokens: int,
    completion_tokens: int,
    prompt_rate: float = 0.0,
    completion_rate: float = 0.0,
) -> float:
    return round((prompt_tokens / 1_000_000 * prompt_rate) + (completion_tokens / 1_000_000 * completion_rate), 6)
