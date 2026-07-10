from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from ingestion.readers import DocumentExtractorBase, FileSystemReader
from utils.domain import Document

logger = logging.getLogger("SentinelIQ.Extractor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TextFileExtractor(DocumentExtractorBase):
    """Production-grade text extractor with robust error handling boundaries."""

    def __init__(self, reader: Optional[FileSystemReader] = None) -> None:
        self.reader = reader or FileSystemReader()

    def extract(self, path: Path) -> Document:
        """Extracts text documents defensively catching system errors."""
        if not path.exists():
            logger.error(f"Target path does not exist for extraction: {path}")
            raise FileNotFoundError(f"Extraction target missing: {path}")

        try:
            # Delegate to core filesystem reader framework
            return self.reader.read(path)
        except PermissionError:
            logger.error(f"System access permissions denied for document: {path}")
            raise PermissionError(f"Access denied reading file: {path.name}")
        except Exception as e:
            logger.error(f"Unexpected file system read failure on document {path.name}: {e}")
            raise IOError(f"Failed extracting raw text from target line: {e}")


class LogStreamExtractor(DocumentExtractorBase):
    """Specialized engine designed to parse line-by-line JSON operational logs safely."""

    def extract(self, path: Path) -> Document:
        """Iterates through JSON lines, isolating corrupted entries dynamically without crashing."""
        valid_records = []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line_idx, line in enumerate(f, 1):
                    line_str = line.strip()
                    if not line_str:
                        continue
                    try:
                        valid_records.append(json.loads(line_str))
                    except json.JSONDecodeError:
                        # Production boundary rule: isolate corrupted trace rows without halting execution
                        logger.warning(f"Malformed operational stream record bypassed at line {line_idx} inside {path.name}")
                        continue

            # Re-compile pristine structured records back to search-indexable content strings
            compiled_content = "\n".join([json.dumps(r) for r in valid_records])
            return Document(
                source_id=f"LOG_{path.stem.upper()}",
                title=path.stem.replace("_", " ").title(),
                content=compiled_content,
                source_path=path,
                metadata={
                    "file_type": ".log",
                    "total_valid_records": str(len(valid_records)),
                    "file_size_bytes": str(path.stat().st_size)
                }
            )
        except Exception as e:
            logger.error(f"Fatal disruption occurred parsing log file {path.name}: {e}")
            raise e