from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large", # or "bge-m3"
)

documents = [
    Document(page_content="The solar system consists of eight planets orbiting a central star.", metadata={"source": "https://gemini.google.com"}),
    Document(page_content="A professional baker requires high-quality flour and precise oven temperatures.", metadata={"source": "https://gemini.google.com"}),
    Document(page_content="Celestial bodies like Mars and Jupiter revolve around the Sun.", metadata={"source": "https://gemini.google.com"}),
    Document(page_content="The secret to a fluffy croissant is cold butter and laminated dough.", metadata={"source": "https://gemini.google.com"})
]

chroma = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="space_and_bread"
)

query = "Tell me about things in outer space"
#query = "What can I eat?"

results = chroma.similarity_search(query, k=2)

print(f"Query: {query}\n")
for idx, doc in enumerate(results):
    print(f"Result {idx + 1}: {doc.page_content} ")