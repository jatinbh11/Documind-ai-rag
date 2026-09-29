import os
import sys

# Ensure UTF-8 output to prevent UnicodeEncodeError on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.embeddings import LocalEmbeddings
from src.vectorstore import LocalVectorStore
from src.retriever import Retriever

def run_test(retriever, query):
    print("========================================")
    print("RETRIEVER TEST")
    print("========================================")
    print(f"\nQuery:\n{query}\n")
    
    try:
        response = retriever.retrieve(query)
        results = response["results"]
        
        print(f"Results:\n{len(results)}\n")
        
        for i, res in enumerate(results):
            print(f"Result {i+1}")
            print("---------")
            print(f"Score: {res['score']:.4f}")
            print(f"Source: {res['source']}")
            print(f"Page: {res['page']}")
            print(f"Chunk: {res['chunk_id']}\n")
            
            # Safely encode the text for Windows console printing
            safe_text = str(res['text']).encode('ascii', errors='replace').decode('ascii')
            print(f"Text:\n{safe_text}\n")
            print("----------------------------------------\n")
            
    except Exception as e:
        print(f"Error during retrieval: {e}")

    print("RETRIEVER TEST COMPLETE")
    print("========================================\n")

def main():
    model_name = "all-MiniLM-L6-v2"
    collection_name = "documind_agentic_ai"
    
    print("Initializing components...")
    try:
        embedder = LocalEmbeddings(model_name)
        vector_store = LocalVectorStore(collection_name=collection_name)
    except Exception as e:
        print(f"Failed to initialize components: {e}")
        return
        
    # Verify collection stats
    collection_info = vector_store.get_collection_info()
    print(f"Verified Qdrant collection points: {collection_info.points_count}\n")
    
    retriever = Retriever(embedder, vector_store, default_threshold=0.20)
    
    # TEST 1
    run_test(retriever, "What is Agentic AI?")
    
    # TEST 2
    run_test(retriever, "What are AI agents?")
    
    # TEST 3 - Unrelated question (should be filtered by threshold)
    run_test(retriever, "What is the capital of France?")
    
    # Outputting formatted context string for demonstration
    print("========================================")
    print("CONTEXT HELPER DEMONSTRATION")
    print("========================================")
    sample_response = retriever.retrieve("What is Agentic AI?", top_k=2)
    formatted_context = retriever.format_context(sample_response["results"])
    safe_context = formatted_context.encode('ascii', errors='replace').decode('ascii')
    print(f"{safe_context}\n")

if __name__ == "__main__":
    main()
