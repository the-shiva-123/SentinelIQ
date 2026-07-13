from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger("SentinelIQ.QualityEngine")

class QualityProfileEngine:
    """Production data profiling engine analyzing raw and ingested assets for quality metrics."""

    def __init__(self, raw_data_dir: Path | str) -> None:
        self.raw_data_dir = Path(raw_data_dir)

    def profile_dataset(self, processed_documents: List[Any]) -> Dict[str, Any]:
        """Runs validation scans over processed document entities to compile an assessment matrix."""
        logger.info("⚡ Executing dataset quality profile scan...")
        
        total_records = len(processed_documents)
        if total_records == 0:
            return {
                "total_records": 0,
                "completeness_rate": 0.0,
                "anomalies_detected": 0,
                "issues_by_file": {}
            }

        anomalous_records = 0
        issues_map: Dict[str, List[str]] = {}

        for doc in processed_documents:
            # Safely check for validation issues attached by the validator stage
            metadata = getattr(doc, "metadata", {})
            issues = metadata.get("validation_issues", [])
            
            if issues:
                anomalous_records += 1
                doc_title = getattr(doc, "title", "Unknown Asset")
                issues_map[doc_title] = issues

        # Calculate exact statistical completeness percentage
        completeness_rate = ((total_records - anomalous_records) / total_records) * 100

        return {
            "total_records": total_records,
            "completeness_rate": round(completeness_rate, 2),
            "anomalies_detected": anomalous_records,
            "issues_by_file": issues_map
        }