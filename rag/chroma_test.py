import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

chroma = chromadb.Client()

collection = chroma.get_or_create_collection(name="my_collection")

collection.upsert(
    ids=["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8"],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is a document about Los Angeles",
        "This is a document about Miami",
        "This is a document about wine",
        "This is a document about Ironman",
        "The capital of France is Paris.", 
        "Pyramids are in Egypt."
    ]
)

# add file
file_path = "wiki_california.txt"
with open(file_path, "r", encoding="utf-8") as file:
    long_text = file.read()

# chunk file
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", " ", ""])
chunks = splitter.split_text(long_text)

# add chunks
collection.add(
    documents=chunks,
    ids=[f"{file_path}_{i}" for i in range(len(chunks))],
    metadatas=[{"source": file_path} for _ in range(len(chunks))]
)

# some queries
results = collection.query(
    query_texts=["This is a query document about Hawaii"],
    n_results=2
)
print(results)

results = collection.query(
    query_texts=["This is a query document about Apple"],
    n_results=2
)
print(results)

results = collection.query(
    query_texts=["Where is the Nile?"],
    n_results=2
)
print(results)

results = collection.query(
    query_texts=["How large is California and what is its capital?"],
    n_results=2
)
print(results)