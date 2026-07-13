from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Union

from ingestion.extractor import TextFileExtractor, LogStreamExtractor, PDFFileExtractor, DocxFileExtractor
from ingestion.repositories import DocumentRepository
from ingestion.validator import DataContractValidator
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
        self.pdf_extractor = PDFFileExtractor()
        self.docx_extractor = DocxFileExtractor()
        self.validator = DataContractValidator()
        
        default_store = DocumentStore()
        self.repository = repository or DocumentRepository(store=default_store)

    def ingest_file(self, path: Union[str, Path]) -> Document:
        """Processes a single document asset, handling text extraction, validation, and storage safely."""
        target_path = Path(path)
        if not target_path.exists():
            logger.error(f"Ingestion aborted. Target file does not exist: {target_path}")
            raise FileNotFoundError(f"File missing at path: {target_path}")

        # Dynamic Routing switch by explicit file suffix extension
        file_extension = target_path.suffix.lower()
        
        if file_extension == ".log":
            document = self.log_extractor.extract(target_path)
        elif file_extension == ".pdf":
            document = self.pdf_extractor.extract(target_path)
        elif file_extension == ".docx":
            document = self.docx_extractor.extract(target_path)
        else:
            document = self.text_extractor.extract(target_path)

        # Strict contract validations check
        result = self.validator.validate(document)
        if not result.is_valid:
            logger.warning(f"Validation constraints triggered for {target_path.name}")
            document.metadata["validation_issues"] = [issue.message for issue in result.issues]

        # Repository layer persistence wrapper
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
                metrics["failed"] += 1
                logger.error(f"❌ Batch pipeline bypassed processing on asset '{Path(path).name}': {batch_error}")
                continue

        logger.info(
            f"🏁 Ingestion run completed. Total: {metrics['attempted']} | "
            f"Success: {metrics['successful']} | Bypassed: {metrics['failed']}"
        )
        return processed_documents