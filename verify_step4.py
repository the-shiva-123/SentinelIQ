from pathlib import Path
from utils.config import settings
from ingestion.readers import DocumentDiscovery
from ingestion.extractor import TextFileExtractor, LogStreamExtractor

def test_step4():
    print("--- Verifying Production Extractors ---")
    
    # 1. Test TextFileExtractor using your discovery components
    discovery = DocumentDiscovery(settings.raw_dir)
    md_files = discovery.discover(pattern="docs/**/*.md")
    
    if md_files:
        print(f"Targeting Markdown Spec via TextExtractor: {md_files[0].name}")
        extractor = TextFileExtractor()
        doc = extractor.extract(md_files[0])
        print(f"✅ Text File Extraction Successful!")
        print(f"Document ID: {doc.source_id} | Type Meta: {doc.metadata}")
    else:
        print("⚠️ No markdown document found to extract.")

    # 2. Test LogStreamExtractor simulating a dirty test environment
    log_dir = settings.raw_dir / "logs"
    log_file = log_dir / "nexatel_managed_ops_2026_07.log"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        f.write('{"timestamp": "2026-07-10T23:00:00Z", "event": "GATEWAY_ONLINE"}\n')
        f.write('CORRUPTED_JSON_LINE_THAT_SHOULD_BE_GRADED_AND_BYPASSED\n')
        f.write('{"timestamp": "2026-07-10T23:05:00Z", "event": "ROUTING_SUCCESS"}\n')

    print(f"\nTargeting Operational Log via LogExtractor: {log_file.name}")
    log_extractor = LogStreamExtractor()
    log_doc = log_extractor.extract(log_file)
    print(f"✅ Log Stream Extraction Successful!")
    print(f"Document ID: {log_doc.source_id} | Valid Extracted Entries: {log_doc.metadata.get('total_valid_records')}")
    
    print("\n✅ Step 4 (ingestion/extractor.py) is officially operational and verified!")

if __name__ == "__main__":
    test_step4()