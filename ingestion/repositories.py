from __future__ import annotations

import logging
from typing import Optional
from utils.domain import Document
from utils.persistence import DocumentStore

logger = logging.getLogger("SentinelIQ.Repository")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DocumentRepository:
    """Production Repository layer handling operations for structural Document ingestion workflows."""

    def __init__(self, store: Optional[DocumentStore] = None) -> None:
        # Defaults to a shared DocumentStore instance if none is provided
        self.store = store or DocumentStore()

    def add(self, document: Document) -> bool:
        """Saves an incoming document asset safely to the persistence framework layer."""
        logger.info(f"Routing Document transaction package '{document.source_id}' to the persistent store...")
        return self.store.save_document(document)

    def find_by_id(self, source_id: str) -> Optional[Document]:
        """Queries the persistent store using a unique source record identifier signature."""
        logger.info(f"Executing storage tracking lookup for unique ID: {source_id}")
        return self.store.get_document(source_id)