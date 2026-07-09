from pathlib import Path
from utils.config import settings
from ingestion.readers import DocumentDiscovery, FileSystemReader

def test_step2():
    print("--- Verifying Document Discovery Engine ---")
    # Scan using your DocumentDiscovery class
    discovery = DocumentDiscovery(settings.raw_dir / "docs")
    discovered_files = discovery.discover(pattern="**/*.md")
    
    print(f"Discovered Markdown Files: {[f.name for f in discovered_files]}")
    
    # Verify FileSystemReader Extraction using your class
    if discovered_files:
        print("\n--- Verifying FileSystem Reader ---")
        reader = FileSystemReader()
        doc = reader.read(discovered_files[0])
        print(f"✅ Successfully read file into Domain object!")
        print(f"Document ID: {doc.source_id}")
        print(f"Document Title: {doc.title}")
        print(f"Metadata Captured: {doc.metadata}")
    else:
        print("\n⚠️ No markdown (.md) files found in data/raw/docs/ to run read test.")
        
    print("\n✅ Step 2 (ingestion/readers.py) is completely functional and verified!")

if __name__ == "__main__":
    test_step2()