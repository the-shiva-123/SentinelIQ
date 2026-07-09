from __future__ import annotations

from pathlib import Path
from typing import Optional

from ingestion.readers import DocumentExtractorBase, FileSystemReader
from utils.domain import Document


class TextFileExtractor(DocumentExtractorBase):
    """Extracts documents from plain text files."""

    def __init__(self, reader: Optional[FileSystemReader] = None) -> None:
        self.reader = reader or FileSystemReader()

    def extract(self, path: Path) -> Document:
        return self.reader.read(path)
