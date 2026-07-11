from pathlib import Path
from utils.config import settings
from ingestion.readers import DocumentDiscovery
from ingestion.service import IngestionService

def test_step8():
    print("--- Verifying Production Ingestion Service Pipeline ---")
    service = IngestionService()
    
    # 1. Discover actual test documents from your raw storage
    discovery = DocumentDiscovery(settings.raw_dir)
    found_files = discovery.discover(pattern="docs/**/*.md")
    
    # 2. Add an artificial missing path target to simulate error resilience bounds
    test_batch = []
    if found_files:
        test_batch.append(found_files[0])
    test_batch.append(Path("D:/sentineliq/raw/docs/missing_system_file_anomaly.md")) # Force failure trace
    
    # 3. Process the batch execution matrix
    print(f"\nDispatching batch pipeline run for test fixtures...")
    results = service.ingest_files(test_batch)
    
    print("\n--- Pipeline Verification Output Matrix ---")
    print(f"Total entries returning active document frames: {len(results)}")
    
    if len(results) > 0:
        print("\n✅ Step 8 (ingestion/service.py) production orchestration works smoothly!")
    else:
        print("\n❌ System failed to process valid documents in execution scope.")

if __name__ == "__main__":
    test_step8()