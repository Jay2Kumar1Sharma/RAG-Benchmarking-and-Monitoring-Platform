import pytest

from app.evaluation.hallucination import HallucinationDetector
from app.models.rag import TextChunk


@pytest.mark.asyncio
async def test_hallucination_detector_flags_unsupported_claims() -> None:
    detector = HallucinationDetector()
    contexts = [TextChunk(id="1", document_id="doc", text="Refunds are available within thirty days.")]

    report = await detector.detect("Refunds are available within thirty days. Support is open on Mars.", contexts)

    assert report.score > 0
    assert report.unsupported_claims
    assert report.unsupported_claim_rate > 0


@pytest.mark.asyncio
async def test_hallucination_detector_validates_citations() -> None:
    detector = HallucinationDetector()
    contexts = [TextChunk(id="1", document_id="doc", text="Access reviews are quarterly.")]

    report = await detector.detect("Access reviews are quarterly [1]. Missing evidence [4].", contexts)

    assert report.citation_coverage == 1.0
    assert report.citation_precision == 0.5
