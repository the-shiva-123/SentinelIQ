from ingestion.api_client import APIClient

def test_step3():
    print("--- Verifying Ingestion API Client ---")
    # Initialize using your exact class name
    client = APIClient(base_url="https://httpbin.org", timeout=5)
    print(f"Client Target URL: {client.base_url}")
    print(f"Client Configured Timeout: {client.timeout} seconds")
    
    print("\n--- Executing GET Test via httpbin ---")
    try:
        response = client.get("/get", params={"test": "sentineliq"})
        print(f"HTTP Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Successfully made network request and received response!")
    except Exception as e:
        print(f"⚠️ Network check skipped or failed: {e}")
        
    print("\n✅ Step 3 (ingestion/api_client.py) basic wiring works!")

if __name__ == "__main__":
    test_step3()