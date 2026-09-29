import logging
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise ImportError("Please install sentence-transformers: pip install sentence-transformers")

logger = logging.getLogger(__name__)

class LocalEmbeddings:
    """
    A simple wrapper for generating local embeddings using SentenceTransformers.
    This module only focuses on TEXT -> VECTOR conversion.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the local embedding model.
        
        Args:
            model_name: The name of the SentenceTransformers model to use.
        """
        logger.info(f"Loading embedding model: {model_name}")
        try:
            # The model is downloaded the first time and cached locally.
            self.model = SentenceTransformer(model_name)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def get_dimension(self) -> int:
        """
        Dynamically detects and returns the dimension of the embeddings produced by this model.
        """
        sample_embedding = self.model.encode("test")
        return len(sample_embedding)

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single text string.
        
        Args:
            text: The text to embed.
            
        Returns:
            The embedding vector as a list of floats.
        """
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text.")
            
        # normalize_embeddings=True standardizes the vector lengths to 1.
        # Normalization is important because it aligns the scale of all vectors, 
        # making distance metrics like dot product directly equivalent to cosine similarity.
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Embeds multiple document chunks.
        
        Args:
            chunks: A list of chunk dictionaries, where each dict has a "text" key.
            
        Returns:
            The same list of chunks, but with a new "embedding" key added to each dict.
        """
        if not chunks:
            raise ValueError("Chunk list is empty.")
            
        texts = [chunk["text"] for chunk in chunks]
        
        # Batch encoding is used here instead of a loop.
        # It's highly efficient because the underlying framework (PyTorch/Transformers)
        # processes multiple inputs in parallel, making optimal use of CPU/GPU resources.
        try:
            embeddings = self.model.encode(texts, normalize_embeddings=True)
        except Exception as e:
            logger.error(f"Failed to generate embeddings for chunks: {e}")
            raise
            
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i].tolist()
            
        return chunks

    def embed_query(self, query: str) -> List[float]:
        """
        Embeds a user query. 
        Uses the exact same model and normalization as the document embeddings.
        This is crucial so that the query and documents are mapped into the exact 
        same mathematical space. If we used a different model, the similarity 
        scores would be meaningless.
        
        Args:
            query: The user query string.
            
        Returns:
            The query embedding vector.
        """
        return self.embed_text(query)
