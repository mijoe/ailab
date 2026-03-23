import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Configuration
DATA_PATH = "policies"
CHROMA_PATH = "db"

def ingest_docs():
    # 1. Load Markdown and PDFs
    # Note: Requires 'pip install "unstructured[md]" pypdf'
    md_loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    
    docs = md_loader.load() + pdf_loader.load()
    print(f"Loaded {len(docs)} documents.")

    # 2. Chunking (Critical for RAG provenance)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=200, # was 100
        add_start_index=True # Helps with tracking 'chunk_id'
    )
    chunks = text_splitter.split_documents(docs)
    
    # 3. Enrich Metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        # Ensure 'source' is just the filename for cleaner citations
        chunk.metadata["source"] = os.path.basename(chunk.metadata.get("source", "unknown"))

    # 4. Embed and Store
    embeddings = OllamaEmbeddings(model="mxbai-embed-large") # model="nomic-embed-text"
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=CHROMA_PATH
    )
    
    print(f"Ingested {len(chunks)} chunks into {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_docs()