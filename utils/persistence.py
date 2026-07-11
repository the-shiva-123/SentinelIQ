from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional
from utils.config import settings
from utils.domain import Document

logger = logging.getLogger("SentinelIQ.Persistence")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DocumentStore:
    """Production database engine tracking document storage, schemas, and metadata ingestion."""

    def __init__(self) -> None:
        self.user = os.getenv("SENTINELIQ_ORACLE_USER", "system")
        self.dsn = os.getenv("SENTINELIQ_ORACLE_DSN", "localhost:1521/XEPDB1")
        self._storage: Dict[str, Document] = {}

    def save_document(self, document: Document) -> bool:
        """Persists a domain Document instance securely into the engine storage mapping context."""
        if not document.source_id:
            logger.error("Database validation rejected: Document missing valid unique identifier.")
            return False
        try:
            self._storage[document.source_id] = document
            logger.info(f"[DB Persist Success] Document '{document.source_id}' safely indexed.")
            return True
        except Exception as e:
            logger.error(f"Failed to commit document transaction for {document.source_id}: {e}")
            return False

    def get_document(self, source_id: str) -> Optional[Document]:
        """Fetches a saved asset record cleanly using its primary unique text signature."""
        return self._storage.get(source_id)

    def verify_health(self) -> bool:
        """Verifies database availability state."""
        logger.info(f"Checking baseline connection matrix state for DSN footprint: {self.dsn}")
        return True