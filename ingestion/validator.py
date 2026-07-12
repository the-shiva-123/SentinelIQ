from __future__ import annotations

import json
import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from utils.config import settings

logger = logging.getLogger("SentinelIQ.Validator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DataContractValidator:
    """Enterprise-grade security checkpoint enforcing input data contracts and manifest validation."""

    def __init__(self, raw_dir: Optional[Path] = None) -> None:
        self.raw_dir = raw_dir or settings.raw_dir
        self.manifest_path = self.raw_dir / "dataset_manifest.json"
        
        # Enforce structural directory subpath extensions matching the contract layout
        self.contract_rules: Dict[str, Set[str]] = {
            "policies": {".pdf"},
            "release_notes": {".docx"},
            "logs": {".log"},
            "docs/architecture": {".md"},
            "docs/architecture/telecom_billing": {".md"},
            "docs/decisions": {".docx", ".md"}
        }

    def validate_manifest(self) -> Dict[str, Any]:
        """Strictly parses and reads the data manifest metadata contract without modifying it."""
        if not self.manifest_path.exists():
            logger.error(f"Critical Ingestion Failure: Manifest file missing at {self.manifest_path}")
            raise FileNotFoundError(f"Dataset contract broken. Missing file: {self.manifest_path}")

        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

            # Enforce mandatory top-level manifest fields explicitly
            required_keys = [
                "dataset_name", "dataset_version", "created_at", "created_by",
                "source_summary", "record_counts", "known_edge_cases", 
                "license_notes", "pii_policy"
            ]
            
            missing_keys = [key for key in required_keys if key not in manifest_data]
            if missing_keys:
                raise ValueError(f"Manifest missing contractual keys: {missing_keys}")

            logger.info(f"✅ Data Manifest Contract verified: {manifest_data['dataset_name']} [v{manifest_data['dataset_version']}]")
            return manifest_data

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Manifest schema validation checks failed: {e}")
            raise ValueError(f"Data manifest structural violation: {e}")

    def calculate_file_hash(self, file_path: Path) -> str:
        """Computes content MD5 hex-digest to catch exact document duplicates."""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def scan_and_validate_directory_assets(self) -> Dict[str, List[Path]]:
        """Scans raw directories, applies file guards, drops bad extensions/empty files, and filters duplicates."""
        seen_content_hashes: Dict[str, Path] = {}
        validated_manifest_files: Dict[str, List[Path]] = {key: [] for key in self.contract_rules.keys()}
        rejected_assets: List[Tuple[Path, str]] = []

        for sub_path, permitted_extensions in self.contract_rules.items():
            target_directory = self.raw_dir / sub_path
            if not target_directory.exists():
                logger.warning(f"Contract directory path skipped (Not Found): {sub_path}")
                continue

            for file_path in target_directory.rglob("*"):
                if not file_path.is_file():
                    continue

                # Guard Rule 1: Extension Contract Verification
                if file_path.suffix.lower() not in permitted_extensions:
                    rejected_assets.append((file_path, f"Unsupported file extension format ({file_path.suffix})"))
                    continue

                # Guard Rule 2: Non-Zero Byte Size Check
                if file_path.stat().st_size == 0:
                    rejected_assets.append((file_path, "Empty/Scratch zero-byte placeholder asset isolated"))
                    continue

                # Guard Rule 3: Precise Cryptographic Deduplication
                content_hash = self.calculate_file_hash(file_path)
                if content_hash in seen_content_hashes:
                    logger.warning(
                        f"Deduplication Filter Active: Skipping duplicate document '{file_path.name}' "
                        f"which mirrors content of '{seen_content_hashes[content_hash].name}'"
                    )
                    continue

                seen_content_hashes[content_hash] = file_path
                validated_manifest_files[sub_path].append(file_path)

        # Print clean, scannable reporting log matrix inside the terminal
        logger.info("--- Data Directory Validation Audit Summary ---")
        for section, parsed_files in validated_manifest_files.items():
            logger.info(f" -> Mapped Category [{section}]: {len(parsed_files)} valid records passed.")

        if rejected_assets:
            logger.warning("--- Defensively Isolated / Quarantined Files ---")
            for asset_path, restriction_reason in rejected_assets:
                logger.warning(f"  [REJECTED] File: {asset_path.name} | Reason: {restriction_reason}")

        return validated_manifest_files