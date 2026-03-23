from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma

# Use the best local embedding model for Ollama
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Strategy A: Structural (The standard reliable way)
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Strategy B: Semantic (Splits based on meaning shifts)
# This calculates the 'distance' between sentences and splits when it's high
semantic_splitter = SemanticChunker(
    embeddings, 
    breakpoint_threshold_type="percentile" # Splits at the 95th percentile of distance
)

file_path = "wiki_california.txt"
with open(file_path, "r", encoding="utf-8") as file:
    long_text = file.read()
docs = [
    Document(page_content=long_text, metadata={"source": file_path})
]

pre_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100
)
intermediate_docs = pre_splitter.split_documents(docs)

# Apply both to a long document
chunks_a = recursive_splitter.split_documents(docs)
chunks_b = semantic_splitter.split_documents(intermediate_docs)

print(chunks_a[0])
print(chunks_b[0])
print(intermediate_docs[0])