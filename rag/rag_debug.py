import chromadb

client = chromadb.PersistentClient(path="./db")  # your actual path
collection = client.get_collection("langchain")

# Fetch chunks around the problem area
results = collection.get(
    where={"chunk_id": {"$in": [18, 19, 20, 21, 22]}},
    include=["documents", "metadatas"]
)

for doc, meta in zip(results["documents"], results["metadatas"]):
    print(f"\n--- chunk_id: {meta.get('chunk_id')} ---")
    print(doc[:300])