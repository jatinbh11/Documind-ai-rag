import logging
from typing import List, Dict, Any

from src.embeddings import LocalEmbeddings
from src.vectorstore import LocalVectorStore

logger = logging.getLogger(__name__)

class Retriever:
    """
    Retrieval layer for fetching relevant document chunks from the vector database.
    Does NOT use external APIs, web search, or LLM generation. It strictly fetches 
    existing context based on vector similarity.
    """
    def __init__(self, embedder: LocalEmbeddings, vector_store: LocalVectorStore, default_threshold: float = 0.20):
        self.embedder = embedder
        self.vector_store = vector_store
        self.default_threshold = default_threshold

    def retrieve(self, query: str, top_k: int = 5, threshold: float = None) -> Dict[str, Any]:
        """
        Retrieves relevant document chunks for a given query from Qdrant.
        Filters results by a similarity threshold.
        """
        if not query or not str(query).strip():
            raise ValueError("Question cannot be empty.")
            
        threshold = threshold if threshold is not None else self.default_threshold
        
        try:
            # 1. Embed the user query
            query_vector = self.embedder.embed_query(query)
            
            # 2. Perform vector search in Qdrant
            raw_results = self.vector_store.search(query_vector=query_vector, limit=top_k)
            
            # 3. Apply retrieval threshold
            filtered_results = []
            for res in raw_results:
                if res["score"] >= threshold:
                    filtered_results.append(res)
                    
            return {
                "query": query,
                "results": filtered_results
            }
        except Exception as e:
            logger.error(f"Retrieval failed for query '{query}': {e}")
            raise

    def format_context(self, retrieved_results: List[Dict[str, Any]]) -> str:
        """
        Converts the list of retrieved result dictionaries into a structured
        context string to be injected into an LLM prompt later.
        """
        context_pieces = []
        for res in retrieved_results:
            source = res.get("source", "Unknown")
            page = res.get("page", "?")
            chunk_id = res.get("chunk_id", "?")
            text = res.get("text", "")
            
            formatted_chunk = f"[Source: {source} | Page: {page} | Chunk: {chunk_id}]\n{text}"
            context_pieces.append(formatted_chunk)
            
        return "\n\n".join(context_pieces)
