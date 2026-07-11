import sys
from utils.config import settings
from ingestion.validatior import DataContractValidator

def test_step5():
    print("--- Running Ingestion Contract Validation Checks ---")
    validator = DataContractValidator()
    
    try:
        # Test 1: Verify Manifest Inspection
        manifest = validator.validate_manifest()
        print("\nManifest Inspection Keys Passed Evaluation:")
        print(f" -> Client/Project Name: {manifest.get('dataset_name')}")
        print(f" -> PII Security Strategy Enforced: {manifest.get('pii_policy')}")
        
        # Test 2: Run Full Directory Isolation & Sanitization Scans
        print("\n--- Triggering System Asset Scan ---")
        valid_map = validator.scan_and_validate_directory_assets()
        
        print("\n✅ Step 5 (ingestion/validatior.py) validation suite successfully compiled!")
        
    except Exception as e:
        print(f"\n❌ Pipeline Contract Failure Detected: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_step5()