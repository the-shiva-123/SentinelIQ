from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Dict, Any
from utils.config import settings
from copilot.graph import CopilotWorkflowGraph

logger = logging.getLogger("SentinelIQ.CopilotEvaluation")

class RAGEvaluator:
    """Production automated evaluation suite checking system answers against reference parameters."""

    def __init__(self) -> None:
        self.reports_dir = Path(getattr(settings, "data_reports_dir", "data/reports"))
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.workflow = CopilotWorkflowGraph().compile_graph()

    def load_seed_dataset(self) -> List[Dict[str, Any]]:
        """Loads reference questions and expected answers to serve as a baseline."""
        return [
            {
                "question": "Which release first introduced ERR_AUTH_401?",
                "expected_answer": "release_notes_NXTEL_2022_Q3_v2.2.0.docx",
                "category": "Security Patching"
            }
        ]

    def run_suite(self) -> Path:
        """Executes test sets, evaluates performance metrics, and writes the markdown summary report."""
        logger.info("🧪 Launching automated RAG evaluation suite execution...")
        seed_data = self.load_seed_dataset()
        report_path = self.reports_dir / "rag_evaluation_v001.md"
        
        results = []
        passed_tests = 0

        for item in seed_data:
            query = item["question"]
            expected = item["expected_answer"]
            
            # Execute through the complete LangGraph pipeline workflow
            output_state = self.workflow.invoke({"query": query})
            generated = output_state["generation_output"]
            
            # Evaluate exact string matching criteria parameters
            is_accurate = expected.lower() in generated.lower()
            if is_accurate:
                passed_tests += 1
                
            results.append({
                "query": query,
                "expected": expected,
                "generated": generated,
                "status": "PASS" if is_accurate else "FAIL"
            })

        # Calculate semantic routing scoring metrics
        accuracy_percentage = (passed_tests / len(seed_data)) * 100
        
        # Compile official performance breakdown summary report
        markdown_report = [
            "# RAG Evaluation Summary Report\n",
            "## Core Performance Tracking Metrics Matrix",
            f"- **Total Test Cases Executed**: {len(seed_data)}",
            f"- **System Accuracy Score**: {accuracy_percentage:.1f}%",
            f"- **Status**: {'SUCCESS' if accuracy_percentage >= 80.0 else 'WARNING'}\n",
            "---",
            "\n## Test Execution Audit Log Breakdown"
        ]

        for idx, res in enumerate(results, start=1):
            markdown_report.extend([
                f"\n### Test Case #{idx}: {res['status']}",
                f"- **Inquiry Prompt**: \"{res['query']}\"",
                f"- **Target Reference Substring**: `{res['expected']}`",
                f"- **System Generative Response Output**: *\"{res['generated']}\"*"
            ])

        report_path.write_text("\n".join(markdown_report), encoding="utf-8")
        logger.info(f"🏁 Automated evaluation completed successfully. Report persisted to: {report_path}")
        return report_path

if __name__ == "__main__":
    evaluator = RAGEvaluator()
    evaluator.run_suite()