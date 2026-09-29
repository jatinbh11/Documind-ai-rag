import os
import uuid
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logger = logging.getLogger(__name__)

class LocalVectorStore:
    def __init__(self, collection_name: str = "documind_agentic_ai", storage_path: str = "local_qdrant_data"):
        """
        Initializes the local Qdrant client. 
        By passing a path, Qdrant runs entirely locally via SQLite/disk without needing Docker or a server.
        """
        self.collection_name = collection_name
        self.storage_path = storage_path
        # Use local persistence
        self.client = QdrantClient(path=self.storage_path)

    def setup_collection(self, vector_dimension: int):
        """
        Creates the collection if it does not exist. 
        Uses COSINE distance because our vectors are normalized, and Cosine is standard for semantic search.
        """
        collections = self.client.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_dimension, distance=Distance.COSINE),
            )
        else:
            # Optionally check if dimensions match
            collection_info = self.client.get_collection(self.collection_name)
            if collection_info.config.params.vectors.size != vector_dimension:
                raise ValueError(f"Existing collection dimension ({collection_info.config.params.vectors.size}) does not match model dimension ({vector_dimension}).")

    def upsert_chunks(self, chunks_with_embeddings: List[Dict[str, Any]]):
        """
        Upserts vectors and metadata into Qdrant.
        Uses deterministic point IDs to avoid duplicating data if run multiple times.
        """
        if not chunks_with_embeddings:
            raise ValueError("No chunks provided to upsert.")

        points = []
        for chunk in chunks_with_embeddings:
            metadata = chunk["metadata"]
            embedding = chunk.get("embedding")
            text = chunk.get("text")
            
            if not embedding:
                raise ValueError(f"Missing embedding for chunk: {metadata.get('chunk_id')}")
                
            # Stable IDs matter so that running this script twice doesn't bloat the database
            # with duplicate vectors. It will instead safely overwrite the existing point.
            chunk_identifier = f"{metadata['source']}_{metadata['chunk_id']}"
            stable_id = str(uuid.uuid5(uuid.NAMESPACE_OID, chunk_identifier))
            
            # Combine text into metadata for the payload
            payload = metadata.copy()
            payload["text"] = text
            
            points.append(
                PointStruct(
                    id=stable_id,
                    vector=embedding,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a vector similarity search using the latest Qdrant query_points API.
        """
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        ).points
        
        formatted_results = []
        for res in search_result:
            formatted_results.append({
                "score": res.score,
                "text": res.payload.get("text"),
                "source": res.payload.get("source"),
                "page": res.payload.get("page"),
                "chunk_id": res.payload.get("chunk_id")
            })
            
        return formatted_results

    def get_collection_info(self):
        return self.client.get_collection(self.collection_name)
