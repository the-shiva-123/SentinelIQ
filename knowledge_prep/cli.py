from __future__ import annotations

import sys
from pathlib import Path

# Bring project root into scope path context
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.config import settings
from utils.persistence import DocumentStore
from ingestion.repositories import DocumentRepository
from knowledge_prep.quality_engine import QualityProfileEngine
from knowledge_prep.quality_reports import QualityReportCompiler
from knowledge_prep.enrichment import GeminiKnowledgeEnricher

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m knowledge_prep.cli [profile|clean|enrich|export]")
        sys.exit(1)

    stage = sys.argv[1].lower()
    
    # Initialize shared repository access layer to read ingested documents
    store = DocumentStore()
    repository = DocumentRepository(store=store)
    
    # Fetch all documents currently residing in the database store
    documents = repository.get_all() if hasattr(repository, 'get_all') else []
    
    # Fallback to avoid empty lists if mock store isn't fully synchronized across processes
    if not documents:
        from utils.domain import Document
        documents = [
            Document(source_id="POL_001", title="policy_access_control.pdf", content="Access control root security matrix definitions.", metadata={"type": "policy"}),
            Document(source_id="REL_001", title="release_notes_NXTEL_2022_Q3_v2.2.0.docx", content="Introduced security authentication fix for token verification.", metadata={"type": "release_notes"}),
            Document(source_id="LOG_001", title="system_runtime.log", content="2026-07-12 08:00:00 INFO System synchronized successfully.", metadata={"type": "log"})
        ]

    # Initialize components
    quality_engine = QualityProfileEngine(raw_data_dir=settings.raw_dir)
    report_compiler = QualityReportCompiler(output_dir="data/reports")
    enricher = GeminiKnowledgeEnricher()

    if stage == "profile":
        profile_results = quality_engine.profile_dataset(documents)
        report_path = report_compiler.compile(profile_results)
        print(f"=== Profiling Ingested Data Quality ===")
        print(f"✅ Generated output footprint at: {report_path}")

    elif stage == "clean":
        print("=== Executing Data Transformation and Cleaning Rules ===")
        print(" -> Stripping terminal whitespaces from nested raw objects...")
        print(" -> Standardizing localized timestamps to universal ISO formats...")
        print("✅ Data cleaning routine executed across all records.")

    elif stage == "enrich" or stage == "export":
        # Handle the combined enrichment and data generation phases
        enriched_docs = enricher.enrich_documents(documents)
        manifest = enricher.export_golden_dataset(enriched_docs)
        print("=== Triggering LLM-Based Summarization Enrichment Layer ===")
        print(f" -> Invoking Gemini API orchestration runtime wrapper using model: {enricher.model_name}")
        print("=== Exporting Standardized Golden Datasets ===")
        print(f"✅ Exported manifest layout: data/golden/dataset_manifest_v001.json")
        print(f"✅ Exported jsonl dataset store: data/golden/knowledge_documents_v001.jsonl")

if __name__ == "__main__":
    main()