from __future__ import annotations

from pathlib import Path
from typing import List

from ingestion.extractor import TextFileExtractor
from ingestion.repositories import DocumentRepository
from ingestion.validator import DocumentValidator
from utils.config import settings
from utils.domain import Document
from utils.persistance import DocumentStore


class IngestionService:
    """High-level orchestration service for ingestion."""

    def __init__(self, repository: DocumentRepository | None = None) -> None:
        self.extractor = TextFileExtractor()
        self.validator = DocumentValidator()
        self.repository = repository or DocumentRepository(DocumentStore(settings.processed_dir))

    def ingest_file(self, path: str | Path) -> Document:
        document = self.extractor.extract(Path(path))
        result = self.validator.validate(document)
        if not result.is_valid:
            document.metadata["validation_issues"] = [issue.message for issue in result.issues]
        self.repository.save(document)
        return document

    def ingest_files(self, paths: List[str | Path]) -> List[Document]:
        return [self.ingest_file(path) for path in paths]
