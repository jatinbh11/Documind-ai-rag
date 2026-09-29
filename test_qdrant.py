import os
import sys

# Ensure UTF-8 output to prevent UnicodeEncodeError on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ingestion import load_pdf, create_chunks
from src.embeddings import LocalEmbeddings
from src.vectorstore import LocalVectorStore

def run_retrieval_test(vector_store, embedder, query_text):
    print("\n========================================")
    print("RETRIEVAL TEST")
    print("==============")
    print(f"\nQuestion:\n{query_text}\n")
    
    query_vector = embedder.embed_query(query_text)
    results = vector_store.search(query_vector, limit=5)
    
    for i, res in enumerate(results):
        print(f"Result {i+1}:")
        print(f"Score:\n{res['score']:.4f}")
        print(f"\nSource:\n{res['source']}")
        print(f"Page:\n{res['page']}")
        print(f"Chunk ID:\n{res['chunk_id']}")
        
        # Safely encode the text for Windows console printing
        safe_text = str(res['text']).encode('ascii', errors='replace').decode('ascii')
        print(f"Text:\n{safe_text}\n")

def main():
    # 1. Ingestion
    pdf_path = os.path.join("data", "agentic-ai.pdf")
    try:
        total_pages, pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)
    except Exception as e:
        print(f"Error loading chunks: {e}")
        return
        
    # 2. Embeddings
    model_name = "all-MiniLM-L6-v2"
    try:
        embedder = LocalEmbeddings(model_name)
        dimension = embedder.get_dimension()
        embedded_chunks = embedder.embed_chunks(chunks)
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return
        
    # 3. Vector Database Initialization
    collection_name = "documind_agentic_ai"
    try:
        vector_store = LocalVectorStore(collection_name=collection_name)
        vector_store.setup_collection(vector_dimension=dimension)
    except Exception as e:
        print(f"Error setting up Qdrant collection: {e}")
        return
        
    # 4. Upsert
    try:
        vector_store.upsert_chunks(embedded_chunks)
    except Exception as e:
        print(f"Error upserting chunks: {e}")
        return
        
    # 5. Check Status
    collection_info = vector_store.get_collection_info()
    
    print("========================================")
    print("QDRANT TEST")
    print("===========")
    print("\nQdrant:\nLOCAL")
    print(f"\nCollection:\n{collection_name}")
    print(f"\nVector dimension:\n{dimension}")
    print(f"\nChunks:\n{len(chunks)}")
    print(f"\nPoints upserted:\n{collection_info.points_count}")
    print("\nCollection status:\nREADY\n")
    
    # 6. Basic Retrieval
    run_retrieval_test(vector_store, embedder, "What is Agentic AI?")
    
    # 7. Second Retrieval Test
    run_retrieval_test(vector_store, embedder, "What are AI agents?")
    
    # 8. Unrelated Question Test
    run_retrieval_test(vector_store, embedder, "What is the capital of France?")
    
    print("\n========================================")
    print("NOTE ON SCORES")
    print("==============")
    print("Qdrant similarity search will still return the mathematically nearest vectors in the ")
    print("vector space, even if the question ('What is the capital of France?') is completely unrelated.")
    print("The score simply represents the cosine distance between the two vectors, NOT logical ")
    print("relevance or LLM confidence. This is why in a complete RAG system, we often set a ")
    print("retrieval threshold to filter out results that are too 'far' mathematically.")

if __name__ == "__main__":
    main()
