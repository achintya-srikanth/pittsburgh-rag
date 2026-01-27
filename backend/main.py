import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient # Added for the smart check

from services.rag import generate_answer
from services.ingestion import ingest_url

# 1. Startup Logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Backend starting up...")
    
    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    collection_name = "pittsburgh_knowledge"
    client = QdrantClient(url=qdrant_url)

    try:
        # Check if collection exists and has data
        collections = client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
        
        # We only seed if the collection is missing OR empty
        needs_seed = True
        if exists:
            info = client.get_collection(collection_name)
            if info.points_count > 0:
                needs_seed = False
                print(f"✅ Knowledge base already contains {info.points_count} vectors. Skipping seed.")

        if needs_seed:
            print("🌱 Knowledge base empty. Starting foundation seed...")
            if os.path.exists("seed_urls.json"):
                with open("seed_urls.json", "r") as f:
                    seeds = json.load(f)
                    for url in seeds:
                        print(f"📥 Ingesting foundation: {url}")
                        ingest_url(url)
                print("✨ Foundation seeding complete!")
            else:
                print("⚠️ seed_urls.json not found. Skipping seed.")

    except Exception as e:
        print(f"⚠️ Startup check failed (Qdrant might still be booting): {e}")
    
    yield
    print("🛑 Backend shutting down...")

# 2. App Initialization
app = FastAPI(lifespan=lifespan)

# 3. Data Models
class QuestionRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    url: str

# 4. Endpoints
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        answer, sources = generate_answer(request.question)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        print(f"❌ RAG Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest(request: IngestRequest):
    try:
        ingest_url(request.url)
        return {"message": "Ingestion successful"}
    except Exception as e:
        print(f"❌ Ingestion Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))