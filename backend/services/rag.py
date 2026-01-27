import os
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient

def generate_answer(question: str):
    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    collection_name = "pittsburgh_knowledge"
    
    # 1. Create the Client
    raw_client = QdrantClient(url=qdrant_url)
    
    # 2. Check if the collection exists
    try:
        collections = raw_client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
    except Exception:
        exists = False
    
    if not exists:
        return "The knowledge base is empty. Please ingest a URL first!", []

    # 3. Initialize Vector Store using the client
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vector_store = QdrantVectorStore(
        client=raw_client,
        collection_name=collection_name,
        embedding=embeddings,
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 4. Setup LLM and Prompt
    llm = ChatOllama(model="llama3", temperature=0, base_url=ollama_url)
    
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful expert on Pittsburgh. Answer the question based ONLY on the following context.
    If the answer is not in the context, say "I don't have that information in my database."
    <context>{context}</context>
    Question: {input}
    Answer:
    """)

    # 5. Build Chain
    # We use a parallel runnable to keep the context for source extraction
    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "input": RunnablePassthrough()}
    )
    
    output_chain = prompt | llm | StrOutputParser()

    # 6. Invoke Chain
    try:
        # Use a variable to store the result of the first invoke
        retrieved_data = {"context": retriever.invoke(question), "input": question}
        answer = (prompt | llm | StrOutputParser()).invoke(retrieved_data)
    
        sources = list(set([doc.metadata.get("source", "unknown") for doc in retrieved_data["context"]]))
        return answer, sources
    except Exception as e:
        return f"Error: {str(e)}", []