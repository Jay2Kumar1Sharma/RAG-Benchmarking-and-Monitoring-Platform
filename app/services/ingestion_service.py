from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import get_logger
from app.database.models import Chunk, Document
from app.database.repositories import DocumentRepository
from app.rag.chunking import ChunkingConfig, build_chunker
from app.rag.document_loaders import LoaderRegistry
from app.rag.factories import build_embedding_provider, build_vector_store
from app.rag.metadata import chunk_fingerprint, metadata_for_upload, read_upload_bytes
from app.schemas.documents import DocumentIngestionItem, DocumentIngestionResponse

logger = get_logger(__name__)
settings = get_settings()
embedding_provider = build_embedding_provider(settings, offline_safe=True)
vector_store = build_vector_store(settings)
ingested_corpus = []


class IngestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = DocumentRepository(session)
        self.loaders = LoaderRegistry()

    async def ingest_uploads(self, files: list[UploadFile]) -> DocumentIngestionResponse:
        items: list[DocumentIngestionItem] = []
        total_chunks = 0
        for file in files:
            item = await self._ingest_one(file)
            items.append(item)
            total_chunks += item.chunks_created
        try:
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            logger.warning("database_persistence_skipped", error=str(exc))
        return DocumentIngestionResponse(documents=items, total_chunks=total_chunks)

    async def _ingest_one(self, file: UploadFile) -> DocumentIngestionItem:
        loader = self.loaders.for_filename(file.filename or "document.txt")
        data = await read_upload_bytes(file)
        text = await loader.load(file)
        metadata = metadata_for_upload(file, data, text)
        document_hash = str(metadata["content_hash"])
        existing = await self._get_existing(document_hash)
        if existing:
            return DocumentIngestionItem(
                filename=file.filename or "document",
                document_id=existing.id,
                chunks_created=0,
                duplicate=True,
            )

        document = Document(
            id=str(uuid4()),
            filename=file.filename or "document",
            content_hash=document_hash,
            mime_type=file.content_type,
            metadata_=metadata,
        )
        try:
            await self.repository.add(document)
        except Exception as exc:
            await self.session.rollback()
            logger.warning("document_db_add_skipped", error=str(exc))
        chunker = build_chunker(
            ChunkingConfig(
                chunk_size=settings.default_chunk_size,
                chunk_overlap=settings.default_chunk_overlap,
            )
        )
        chunks = chunker.split(
            text,
            document.id,
            {"filename": document.filename, "content_hash": document_hash},
        )
        for chunk in chunks:
            chunk.metadata["fingerprint"] = chunk_fingerprint(
                document_hash,
                chunk.text,
                int(chunk.metadata["chunk_index"]),
            )
        vectors = await embedding_provider.embed_batches([chunk.text for chunk in chunks])
        await vector_store.upsert("default", chunks, vectors)
        ingested_corpus.extend(chunks)
        for chunk in chunks:
            self.session.add(
                Chunk(
                    id=chunk.id,
                    document_id=document.id,
                    chunk_index=int(chunk.metadata["chunk_index"]),
                    text=chunk.text,
                    metadata_=chunk.metadata,
                    embedding_model=embedding_provider.model_name,
                    vector_id=chunk.id,
                )
            )
        return DocumentIngestionItem(
            filename=document.filename,
            document_id=document.id,
            chunks_created=len(chunks),
            metadata=metadata,
        )

    async def _get_existing(self, content_hash: str) -> Document | None:
        try:
            return await self.repository.get_by_hash(content_hash)
        except Exception as exc:
            await self.session.rollback()
            logger.warning("duplicate_lookup_skipped", error=str(exc))
            return None
