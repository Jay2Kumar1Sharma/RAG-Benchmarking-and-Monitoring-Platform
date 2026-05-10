from app.core.config import Settings
from app.rag.generation import GeminiLLM, GroqLLM, LLMProvider, MockGroundedLLM, OpenAILLM


def build_llm_provider(settings: Settings) -> LLMProvider:
    if settings.default_llm_provider == "gemini":
        return GeminiLLM(settings.gemini_api_key, settings.gemini_model)
    if settings.default_llm_provider == "openai":
        return OpenAILLM()
    if settings.default_llm_provider == "groq":
        return GroqLLM()
    return MockGroundedLLM()
