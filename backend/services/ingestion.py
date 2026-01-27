import os
import requests
from bs4 import BeautifulSoup
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def ingest_url(url: str):
    # 1. Scrape the content
    # Adding a header makes the request look like a real browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Clean up text: remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=' ')

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=t, metadata={"source": url}) for t in chunks]

    # 3. Setup Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create/Update Vector Store using the Explicit Client
    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    raw_client = QdrantClient(url=qdrant_url)

    QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    client=raw_client,
    collection_name="pittsburgh_knowledge"
    )
    return True