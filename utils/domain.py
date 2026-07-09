from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class Document:
    """Represents a document loaded during the ingestion flow."""

    source_id: str
    title: str
    content: str
    source_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    @property
    def identifier(self) -> str:
        return self.source_id
