# 🏙️ Pittsburgh Knowledge Assistant

A full-stack RAG (Retrieval-Augmented Generation) application that allows users to ingest local knowledge (URLs) into a Qdrant vector database and query it using Llama 3 via Ollama.

## 🚀 Features
* **Web Scraping:** Ingest any URL to expand the AI's knowledge.
* **Vector Search:** Uses `all-MiniLM-L6-v2` embeddings for semantic search in Qdrant.
* **Local LLM:** Powered by Ollama (Llama 3) for 100% private, local inference.
* **Containerized:** Entire stack runs via Docker Compose.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Orchestration:** LangChain
- **Vector DB:** Qdrant
- **LLM:** Ollama (Llama 3)

## 📦 Getting Started

### Prerequisites
1. Install [Docker & Docker Compose](https://docs.docker.com/get-docker/).
2. Install [Ollama](https://ollama.com/) on your host machine.
3. Pull the model: `ollama pull llama3`.

### Installation
1. Clone the repo:

   git clone [https://github.com/achintya-srikanth/pittsburgh-rag.git](https://github.com/achintya-srikanth/pittsburgh-rag.git)
   cd pittsburgh-rag

2. Start the services:

    docker-compose up --build

3. Access the apps:

    - UI: http://localhost:8501
    - Backend API: http://localhost:8000
    - Qdrant Dashboard: http://localhost:6333/dashboard

4. Ask away! Ingest more URLs for more specific searches.

### 🗺️ Roadmap & Future Improvements

To move this from a prototype to a production-grade system, the following features are planned:

### 1. Advanced Retrieval: The Reranker
- **Goal:** Improve precision by rescoring the top-k results.
- **Why:** Standard vector search (Cosine Similarity) is fast but sometimes misses nuance. Adding a **Cross-Encoder reranker** (like `BGE-Reranker`) ensures the most contextually relevant chunks are prioritized before being sent to the LLM.

### 2. Objective Evaluation (RAGAS Framework)
- **Goal:** Move from "vibe-based" testing to mathematical metrics.
- **Why:** Use [RAGAS](https://docs.ragas.io/) to measure **Faithfulness** (hallucination check), **Answer Relevance**, and **Context Precision**. This allows for data-driven improvements to the prompt and chunking strategy.

### 3. Multimodal Ingestion
- **Goal:** Support images, charts, and PDFs.
- **Why:** Pittsburgh's history and data are often locked in scanned maps or architectural diagrams. Integrating **OCR** and **CLIP embeddings** will allow the assistant to "see" and describe visual data.

### 4. Model-Agnostic Inference Layer
- **Goal:** Seamlessly switch between local (Ollama) and cloud (OpenAI/Anthropic) models.
- **Why:** Different use cases require different trade-offs between cost, privacy, and reasoning power. Implementing a unified interface will make the system future-proof.

### 5. Persistent Chat Memory
- **Goal:** Maintain conversation context across multiple turns.
- **Why:** Allow users to ask follow-up questions like "Tell me more about the first point" without re-stating the entire topic.
