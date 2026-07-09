from __future__ import annotations

from pathlib import Path
from typing import List

from utils.domain import Document
from utils.persistance import DocumentStore


class DocumentRepository:
    """Repository layer for storing and retrieving documents."""

    def __init__(self, store: DocumentStore) -> None:
        self.store = store

    def save(self, document: Document) -> Path:
        return self.store.save(document)

    def list_documents(self) -> List[Document]:
        documents: List[Document] = []
        for source_id in self.store.list_ids():
            payload = self.store.load(source_id)
            documents.append(
                Document(
                    source_id=payload.get("source_id", source_id),
                    title=payload.get("title", source_id),
                    content=payload.get("content", ""),
                    metadata=payload.get("metadata", {}),
                    tags=payload.get("tags", []),
                )
            )
        return documents
