from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    """Application settings used by ingestion and downstream services."""

    data_dir: Path = Path(__file__).resolve().parents[1] / "data"
    raw_dir: Path = data_dir / "raw"
    processed_dir: Path = data_dir / "processed"
    logs_dir: Path = data_dir / "logs"
    evaluation_dir: Path = data_dir / "evaluation"
    golden_dir: Path = data_dir / "golden"
    manifest_path: Path = raw_dir / "dataset_manifest.json"

    api_base_url: Optional[str] = None
    api_timeout_seconds: int = 30

    def __post_init__(self) -> None:
        self.data_dir = Path(os.getenv("SENTINELIQ_DATA_DIR", str(self.data_dir)))
        self.raw_dir = Path(os.getenv("SENTINELIQ_RAW_DIR", str(self.raw_dir)))
        self.processed_dir = Path(os.getenv("SENTINELIQ_PROCESSED_DIR", str(self.processed_dir)))
        self.logs_dir = Path(os.getenv("SENTINELIQ_LOGS_DIR", str(self.logs_dir)))
        self.evaluation_dir = Path(os.getenv("SENTINELIQ_EVALUATION_DIR", str(self.evaluation_dir)))
        self.golden_dir = Path(os.getenv("SENTINELIQ_GOLDEN_DIR", str(self.golden_dir)))
        self.manifest_path = Path(os.getenv("SENTINELIQ_MANIFEST_PATH", str(self.manifest_path)))
        self.api_base_url = os.getenv("SENTINELIQ_API_BASE_URL", self.api_base_url)
        self.api_timeout_seconds = int(os.getenv("SENTINELIQ_API_TIMEOUT_SECONDS", self.api_timeout_seconds))


settings = Settings()
