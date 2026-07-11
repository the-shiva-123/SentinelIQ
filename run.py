from __future__ import annotations

import logging
import sys
from pathlib import Path

from utils.config import settings
from ingestion.readers import DocumentDiscovery
from ingestion.service import IngestionService

# Configure master logging for application execution output
logger = logging.getLogger("SentinelIQ.Main")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def bootstrap_pipeline() -> None:
    """Bootstraps and runs the entire SentinelIQ data ingestion pipeline workspace."""
    logger.info("====================================================")
    logger.info("Initializing SentinelIQ Data Ingestion System Workspace")
    logger.info("====================================================")
    
    # 1. Initialize our Document Discovery Engine (Step 3)
    logger.info(f"Scanning raw target workspace directory: {settings.raw_dir}")
    discovery = DocumentDiscovery(settings.raw_dir)
    
    # Discover all target documents recursively across matching extensions
    discovered_files = discovery.discover(pattern="**/*.*")
    
    if not discovered_files:
        logger.warning("No operational assets or raw documents matched the current directory scan.")
        logger.info("Pipeline processing completed: Zero tasks pending.")
        return

    logger.info(f"Discovery engine successfully identified {len(discovered_files)} potential workspace assets.")

    # 2. Instantiate our Core Orchestration Service (Step 8)
    pipeline_service = IngestionService()

    # 3. Trigger full batch processing execution flow
    try:
        processed_docs = pipeline_service.ingest_files(discovered_files)
        
        logger.info("====================================================")
        logger.info("Execution Summary Metrics Matrix:")
        logger.info(f" -> Total Assets Ingestion Batch Scope: {len(discovered_files)}")
        logger.info(f" -> Total Documents Successfully Persisted: {processed_documents_count(processed_docs)}")
        logger.info("====================================================")
        logger.info("🎉 SentinelIQ Data Pipeline execution completed successfully!")
        
    except Exception as fatal_err:
        logger.critical(f"🛑 Critical Pipeline Disruption Occurred during runtime: {fatal_err}")
        sys.exit(1)


def processed_documents_count(docs) -> int:
    """Helper metrics filter verifying successfully saved document footprints."""
    return len([d for d in docs if "validation_issues" not in d.metadata])


if __name__ == "__main__":
    bootstrap_pipeline()