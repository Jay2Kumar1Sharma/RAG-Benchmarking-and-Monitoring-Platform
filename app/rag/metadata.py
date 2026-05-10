import hashlib
from pathlib import Path

from fastapi import UploadFile


async def read_upload_bytes(file: UploadFile) -> bytes:
    data = await file.read()
    await file.seek(0)
    return data


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def metadata_for_upload(file: UploadFile, data: bytes, extracted_text: str) -> dict[str, object]:
    filename = file.filename or "document"
    suffix = Path(filename).suffix.lower()
    return {
        "filename": filename,
        "extension": suffix,
        "mime_type": file.content_type,
        "byte_size": len(data),
        "text_chars": len(extracted_text),
        "content_hash": content_hash(data),
        "line_count": extracted_text.count("\n") + 1 if extracted_text else 0,
    }


def chunk_fingerprint(document_hash: str, chunk_text: str, chunk_index: int) -> str:
    payload = f"{document_hash}:{chunk_index}:{chunk_text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

