import os
import sys
import numpy as np

# Ensure we can import from src directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ingestion import load_pdf, create_chunks
from src.embeddings import LocalEmbeddings

def cosine_similarity(vec_a, vec_b):
    """Calculates the cosine similarity between two vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    # Vectors are pre-normalized, so dot product would technically be enough,
    # but using full formula to strictly demonstrate cosine similarity calculation.
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():
    print("========================================")
    print("EMBEDDING TEST")
    print("==============")

    model_name = "all-MiniLM-L6-v2"
    print(f"\nEmbedding model: {model_name}")
    
    # 1. Use existing ingestion pipeline to get chunks
    pdf_path = os.path.join("data", "agentic-ai.pdf")
    try:
        total_pages, pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return

    print(f"\nNumber of chunks:\n{len(chunks)}")

    # 2. Initialize Embedder
    print("\nLoading embedding model (this may take a moment to download on first run)...")
    try:
        embedder = LocalEmbeddings(model_name)
    except Exception as e:
        print(f"Error initializing embedder: {e}")
        return

    # 3. Detect dimension dynamically
    actual_dimension = embedder.get_dimension()
    print(f"\nEmbedding dimension: {actual_dimension}")

    # 4. Embed chunks
    try:
        embedded_chunks = embedder.embed_chunks(chunks)
    except Exception as e:
        print(f"Error embedding chunks: {e}")
        return

    first_vector = embedded_chunks[0]["embedding"]
    print(f"\nFirst vector length: {len(first_vector)}")
    print(f"\nFirst 5 vector values:\n{first_vector[:5]}")

    print("\n========================================")
    print("QUERY TEST")
    print("==========")
    
    query = "What is Agentic AI?"
    print(f"\nQuery:\n{query}")
    
    query_vector = embedder.embed_query(query)
    query_dimension = len(query_vector)
    print(f"\nQuery vector dimension: {query_dimension}")
    
    print("\nDimension check:")
    if query_dimension == actual_dimension:
        print("PASS")
    else:
        print(f"FAIL: Query dimension ({query_dimension}) does not match document dimension ({actual_dimension}).")
        
    print("\n========================================")
    print("SIMILARITY TEST")
    print("===============")
    
    sentence_a = "What is an AI agent?"
    sentence_b = "How do autonomous AI agents work?"
    sentence_c = "What is the capital of France?"
    
    vec_a = embedder.embed_text(sentence_a)
    vec_b = embedder.embed_text(sentence_b)
    vec_c = embedder.embed_text(sentence_c)
    
    sim_a_b = cosine_similarity(vec_a, vec_b)
    sim_a_c = cosine_similarity(vec_a, vec_c)
    
    print(f"\nA vs B:\n{sim_a_b:.4f}")
    print(f"\nA vs C:\n{sim_a_c:.4f}")
    
    print("\nNote: Similarity values depend on the embedding model, text, preprocessing, normalization, and similarity metric.")

    print("\n========================================")
    print("EMBEDDING TEST COMPLETE")
    print("=======================")

if __name__ == "__main__":
    main()
