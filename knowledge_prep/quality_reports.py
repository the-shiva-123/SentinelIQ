from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("SentinelIQ.QualityReports")

class QualityReportCompiler:
    """Compiles programmatic data profiling metrics into human-readable Markdown documentation."""

    def __init__(self, output_dir: Path | str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compile(self, profile_results: Dict[str, Any], filename: str = "data_quality_summary.md") -> Path:
        """Transforms metric matrices into a structured Markdown summary file."""
        report_path = self.output_dir / filename
        logger.info(f"📝 Compiling data quality report to {report_path}...")

        markdown_content = [
            "# Data Quality Summary Report\n",
            "## Executive Summary Metrics Matrix",
            f"- **Total Records Analyzed**: {profile_results.get('total_records', 0)}",
            f"- **Completeness Rate**: {profile_results.get('completeness_rate', 0.0)}%",
            f"- **Identified Anomalies**: {profile_results.get('anomalies_detected', 0)} quarantined structural assets.\n",
            "---",
            "\n## Detailed Issues Log By File Asset"
        ]

        issues_map = profile_results.get("issues_by_file", {})
        if not issues_map:
            markdown_content.append("\n✅ All tracked assets passed core contract structural validations cleanly.")
        else:
            for file_title, issues in issues_map.items():
                markdown_content.append(f"\n### ❌ {file_title}")
                for issue in issues:
                    markdown_content.append(f"- Triggered Constraint: {issue}")

        # Persist the markdown report to disk
        report_path.write_text("\n".join(markdown_content), encoding="utf-8")
        logger.info("🎉 Report compilation successfully completed.")
        return report_path