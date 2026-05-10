import hashlib

from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import get_logger
from app.database.models import Chunk, Document
from app.database.repositories import DocumentRepository
from app.rag.chunking import ChunkingConfig, build_chunker
from app.rag.document_loaders import LoaderRegistry
from app.rag.embeddings import CachedEmbeddingProvider, HashEmbeddingProvider
from app.rag.vectorstores import InMemoryVectorStore
from app.schemas.documents import DocumentIngestionItem, DocumentIngestionResponse

logger = get_logger(__name__)
settings = get_settings()
embedding_provider = CachedEmbeddingProvider(
    HashEmbeddingProvider(model_name=settings.default_embedding_model)
)
vector_store = InMemoryVectorStore()
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
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.warning("database_persistence_skipped", error=str(exc))
        return DocumentIngestionResponse(documents=items, total_chunks=total_chunks)

    async def _ingest_one(self, file: UploadFile) -> DocumentIngestionItem:
        loader = self.loaders.for_filename(file.filename or "document.txt")
        text = await loader.load(file)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing = await self._get_existing(content_hash)
        if existing:
            return DocumentIngestionItem(
                filename=file.filename or "document",
                document_id=existing.id,
                chunks_created=0,
                duplicate=True,
            )

        document = Document(
            filename=file.filename or "document",
            content_hash=content_hash,
            mime_type=file.content_type,
            metadata_={},
        )
        try:
            await self.repository.add(document)
        except SQLAlchemyError as exc:
            logger.warning("document_db_add_skipped", error=str(exc))
        chunker = build_chunker(
            ChunkingConfig(chunk_size=settings.default_chunk_size, chunk_overlap=settings.default_chunk_overlap)
        )
        chunks = chunker.split(text, document.id, {"filename": document.filename, "content_hash": content_hash})
        vectors = await embedding_provider.embed_texts([chunk.text for chunk in chunks])
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
            metadata={"hash": content_hash},
        )

    async def _get_existing(self, content_hash: str) -> Document | None:
        try:
            return await self.repository.get_by_hash(content_hash)
        except SQLAlchemyError:
            return None
