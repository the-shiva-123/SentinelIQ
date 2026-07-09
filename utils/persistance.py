from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from utils.domain import Document


class DocumentStore:
    """Persists ingested documents as JSON files on disk."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, document: Document) -> Path:
        target = self.root / f"{document.source_id}.json"
        payload = {
            "source_id": document.source_id,
            "title": document.title,
            "content": document.content,
            "metadata": document.metadata,
            "tags": document.tags,
        }
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def load(self, source_id: str) -> Dict[str, Any]:
        target = self.root / f"{source_id}.json"
        return json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}

    def list_ids(self) -> List[str]:
        return [path.stem for path in self.root.glob("*.json")]
