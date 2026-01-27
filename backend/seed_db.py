import json
import requests
import time

# This line pretends to be a user and sends all URLs to the API
# API_URL = "http://localhost:8000/ingest"

# Get URL from environment, default to internal docker service name
API_URL = os.getenv("API_URL", "http://backend:8000/ingest")

def seed():
    with open("seed_data.json", "r") as f:
        urls = json.load(f)

    print(f"🌱 Found {len(urls)} URLs to ingest...")

    for url in urls:
        try:
            print(f"Ingesting: {url}...", end=" ")
            response = requests.post(API_URL, json={"url": url})
            if response.status_code == 200:
                print("✅ Done")
            else:
                print(f"❌ Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    print("🚀 Seeding complete!")

if __name__ == "__main__":
    # Wait for the backend to start up before seeding
    time.sleep(5) 
    seed()