from __future__ import annotations

from pathlib import Path
from typing import Iterator, List, Optional, Sequence

from utils.domain import Document


class Reader:
    """Base interface for document readers."""

    def read(self, path: Path) -> Document:
        raise NotImplementedError


class FileSystemReader(Reader):
    """Reads text files from disk."""

    def read(self, path: Path) -> Document:
        content = path.read_text(encoding="utf-8")
        return Document(
            source_id=path.stem,
            title=path.stem,
            content=content,
            source_path=path,
            metadata={"file_type": path.suffix.lower()},
        )


class DocumentDiscovery:
    """Finds candidate files for ingestion."""

    def __init__(self, root: Path):
        self.root = root

    def discover(self, pattern: str = "**/*") -> List[Path]:
        return sorted(self.root.glob(pattern))


class DocumentExtractorBase:
    """Base class for extracting content from input files."""

    def extract(self, path: Path) -> Document:
        raise NotImplementedError
