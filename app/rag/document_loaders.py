from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile


class DocumentLoader(ABC):
    supported_suffixes: set[str]

    @abstractmethod
    async def load(self, file: UploadFile) -> str:
        raise NotImplementedError


class PlainTextLoader(DocumentLoader):
    supported_suffixes = {".txt", ".md", ".markdown"}

    async def load(self, file: UploadFile) -> str:
        data = await file.read()
        return data.decode("utf-8", errors="replace")


class PdfLoader(DocumentLoader):
    supported_suffixes = {".pdf"}

    async def load(self, file: UploadFile) -> str:
        from pypdf import PdfReader

        reader = PdfReader(file.file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)


class DocxLoader(DocumentLoader):
    supported_suffixes = {".docx"}

    async def load(self, file: UploadFile) -> str:
        from docx import Document

        document = Document(file.file)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)


class OcrReadyLoader(DocumentLoader):
    """Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR."""

    supported_suffixes = {".png", ".jpg", ".jpeg", ".tiff"}

    async def load(self, file: UploadFile) -> str:
        raise NotImplementedError("OCR provider is not configured for local mode.")


class LoaderRegistry:
    def __init__(self) -> None:
        self.loaders = [PlainTextLoader(), PdfLoader(), DocxLoader()]

    def for_filename(self, filename: str) -> DocumentLoader:
        suffix = Path(filename).suffix.lower()
        for loader in self.loaders:
            if suffix in loader.supported_suffixes:
                return loader
        raise ValueError(f"Unsupported document type: {suffix or filename}")

