from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Union

from ingestion.extractor import TextFileExtractor, LogStreamExtractor
from ingestion.repositories import DocumentRepository
from ingestion.validator import DocumentValidator
from utils.config import settings
from utils.domain import Document
from utils.persistence import DocumentStore

logger = logging.getLogger("SentinelIQ.IngestionService")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class IngestionService:
    """Production-grade high-level orchestration service for data ingestion."""

    def __init__(self, repository: DocumentRepository | None = None) -> None:
        self.text_extractor = TextFileExtractor()
        self.log_extractor = LogStreamExtractor()
        self.validator = DocumentValidator()
        
        # Initialize default store targeting the configured repository path
        default_store = DocumentStore()
        self.repository = repository or DocumentRepository(store=default_store)

    def ingest_file(self, path: Union[str, Path]) -> Document:
        """Processes a single document asset, handling text extraction, validation, and storage safely."""
        target_path = Path(path)
        if not target_path.exists():
            logger.error(f"Ingestion aborted. Target file does not exist: {target_path}")
            raise FileNotFoundError(f"File missing at path: {target_path}")

        # Rule 1: Dynamic Routing based on file layout rules
        if target_path.suffix.lower() == ".log":
            document = self.log_extractor.extract(target_path)
        else:
            document = self.text_extractor.extract(target_path)

        # Rule 2: Strict contract validations check
        result = self.validator.validate(document)
        if not result.is_valid:
            logger.warning(f"Validation constraints triggered for {target_path.name}")
            document.metadata["validation_issues"] = [issue.message for issue in result.issues]

        # Rule 3: Repository layer persistence wrapper
        success = self.repository.add(document)
        if not success:
            raise IOError(f"Database rejected document commit sequence: {document.source_id}")

        return document

    def ingest_files(self, paths: List[Union[str, Path]]) -> List[Document]:
        """Runs batch processing loops defensively to ensure single-file anomalies don't halt execution."""
        processed_documents: List[Document] = []
        metrics = {"attempted": 0, "successful": 0, "failed": 0}

        logger.info(f"🚀 Launching batch processing run for {len(paths)} target assets...")

        for path in paths:
            metrics["attempted"] += 1
            try:
                doc = self.ingest_file(path)
                processed_documents.append(doc)
                metrics["successful"] += 1
            except Exception as batch_error:
                # Production Boundary Guard: Log the specific file break, but keep the pipeline processing the rest
                metrics["failed"] += 1
                logger.error(f"❌ Batch pipeline bypassed processing on asset '{Path(path).name}': {batch_error}")
                continue

        logger.info(
            f"🏁 Ingestion run completed. Total: {metrics['attempted']} | "
            f"Success: {metrics['successful']} | Bypassed: {metrics['failed']}"
        )
        return processed_documents