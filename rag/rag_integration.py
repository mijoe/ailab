from dataclasses import dataclass
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import re

@dataclass
class RetrievedChunk:
    source_doc: str
    chunk_id: int
    score: float
    metadata: Dict[str, Any]
    content: str

@dataclass
class RAGResult:
    answer: str
    citations: List[Dict[str, Any]]
    verified: bool

class ContextAssembler:
    @staticmethod
    def assemble(chunks: List[RetrievedChunk]) -> str:
        context_blocks = []
        for i, chunk in enumerate(chunks, 1):
            block = f"Source [{i}] (File: {chunk.source_doc}):\n{chunk.content}"
            context_blocks.append(block)
        return "\n\n---\n\n".join(context_blocks)

class RAGEngine:
    def __init__(self, db_path: str):
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large") # model="nomic-embed-text"
        self.db = Chroma(persist_directory=db_path, embedding_function=self.embeddings)
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0) # model="llama3.2"

    def query(self, question: str, k: int = 3) -> RAGResult:
        # 1. Retrieve
        docs_with_scores = self.db.similarity_search_with_relevance_scores(question, k=k)
        
        chunks = [
            RetrievedChunk(
                source_doc=doc.metadata.get("source", "unknown"),
                chunk_id=doc.metadata.get("chunk_id", 0),
                score=score,
                metadata=doc.metadata,
                content=doc.page_content
            ) for doc, score in docs_with_scores
        ]

        # 2. Assemble Context
        context_text = ContextAssembler.assemble(chunks)

        # 3. Generate with Citation Instructions
        # system_prompt = (
        #     "You are a helpful assistant. Answer the question using ONLY the provided context. "
        #     "Every statement must cite the source number like [Source 1]. Every claim must be cited inline "
        #     "at the point it is made. Do not add a summary citation at the end. If the context doesn't "
        #     "contain the answer, say you don't know."
        # )
        system_prompt = ("""You are a security policy assistant. Answer using ONLY the provided sources.

            CITATION RULES — MANDATORY:
            1. Every sentence or bullet point that contains a factual claim MUST end with [Source N]
            where N is the number of the source it came from.
            2. Each bullet point gets its own citation. Do not group multiple bullets under one citation.
            3. Never cite a source for a claim unless that source explicitly contains that information.
            4. If a claim draws from multiple sources, cite all of them: [Source 1][Source 2].
            5. Do not add a summary citation at the end. Citations belong inline only.

            Sources:
            {context}

            Question: {question}"""
        )

        user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        # 4. Verify & Format Output
        citations = [
            {"source": c.source_doc, "chunk_id": c.chunk_id, "excerpt": c.content}
            for c in chunks
        ]

        verified_citations = verify_citations(response.content, citations)
        print(verified_citations)

        uncited_sources = check_uncited_sources(response.content, citations)
        print(uncited_sources)

        return RAGResult(
            answer=response.content,
            citations=citations,
            verified=verified_citations['verified']
        )

def verify_citations(answer: str, citations: list[dict]) -> dict:
    """
    For each cited [Source N] in the answer, extract the surrounding
    sentence and check it against the source chunk text.
    Returns: {verified: bool, details: list[dict]}
    """
    
    results = []
    
    # Find every [Source N] reference and the sentence containing it
    sentences = re.split(r'(?<=[.!?])\s+', answer)
    
    for sentence in sentences:
        matches = re.findall(r'\[Source (\d+)\]', sentence)
        for match in matches:
            source_idx = int(match) - 1  # 0-indexed
            if source_idx >= len(citations):
                results.append({
                    "citation": f"[Source {match}]",
                    "sentence": sentence,
                    "verdict": "INVALID",  # cited non-existent source
                    "reason": f"Source {match} does not exist in retrieved chunks"
                })
                continue
            
            chunk_text = citations[source_idx]["excerpt"].lower()
            
            # Extract key noun phrases from the sentence (simplified)
            # Check if meaningful words from the sentence appear in the chunk
            sentence_words = set(
                w.lower() for w in re.findall(r'\b[a-zA-Z]{5,}\b', sentence)
                if w.lower() not in {"should", "must", "states", "according", 
                                     "policy", "which", "their", "these", "those"}
            )
            chunk_words = set(re.findall(r'\b[a-zA-Z]{5,}\b', chunk_text))
            
            overlap = sentence_words & chunk_words
            overlap_ratio = len(overlap) / max(len(sentence_words), 1)
            
            results.append({
                "citation": f"[Source {match}]",
                "sentence": sentence[:100],
                "overlap_ratio": round(overlap_ratio, 2),
                "matched_terms": list(overlap)[:5],
                "verdict": "SUPPORTED" if overlap_ratio > 0.25 else "UNSUPPORTED"
            })
    
    all_supported = all(r["verdict"] == "SUPPORTED" for r in results)
    return {
        "verified": all_supported,
        "citation_count": len(results),
        "details": results
    }

# After checking inline citations, also check for uncited source usage
def check_uncited_sources(answer: str, citations: list[dict]) -> list[str]:
    """
    Check if content from a retrieved chunk appears in the answer
    but was never cited.
    """
    cited_indices = set(
        int(m) - 1  # 0-indexed
        for m in re.findall(r'\[Source (\d+)\]', answer)
    )
    
    uncited = []
    for i, chunk in enumerate(citations):
        if i in cited_indices:
            continue  # already cited, skip
        
        # Check if meaningful terms from this chunk appear in the answer
        chunk_words = set(
            w.lower() for w in re.findall(r'\b[a-zA-Z]{6,}\b', chunk["excerpt"])
        )
        answer_words = set(
            w.lower() for w in re.findall(r'\b[a-zA-Z]{6,}\b', answer)
        )
        overlap = chunk_words & answer_words
        
        if len(overlap) >= 3:  # meaningful overlap threshold
            uncited.append({
                "source_idx": i + 1,
                "source": chunk["source"],
                "matched_terms": list(overlap)[:5],
                "verdict": "CONTENT_USED_WITHOUT_CITATION"
            })
    
    return uncited

# Run
rag = RAGEngine('./db')

# Test
result = rag.query("What is our policy on third-party vendor access?")
print(result.answer)      # coherent answer
print(result.citations)   # [{"source": "vendor_policy.pdf", "chunk_id": 3, "excerpt": "..."}]
print(result.verified)    # True/False — did the LLM actually use these sources?