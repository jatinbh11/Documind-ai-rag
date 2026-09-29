import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graph import RAGGraph

def test_query(graph_runner, query: str):
    print("========================================")
    print("LANGGRAPH TEST")
    print("========================================")
    print(f"\nQuestion:\n{query}\n")
    
    try:
        final_state = graph_runner.run(query)
        
        print(f"Has context:\n{final_state.get('has_context')}\n")
        print(f"Retrieved chunks:\n{len(final_state.get('retrieved_context', []))}\n")
        
        executed = "EXECUTED" if final_state.get('generate_node_executed') else "NOT EXECUTED"
        print(f"Generation node:\n{executed}\n")
        
        answer = final_state.get('answer', 'EMPTY')
        print(f"Answer:\n{answer}\n")
        
    except Exception as e:
        print(f"Error during graph execution: {e}")

    print("----------------------------------------\n")

def main():
    print("Initializing LangGraph orchestrator...")
    try:
        graph_runner = RAGGraph()
    except Exception as e:
        print(f"Failed to initialize components: {e}")
        return
        
    # TEST 1
    test_query(graph_runner, "What is Agentic AI?")
    
    # TEST 2
    test_query(graph_runner, "What are AI agents?")
    
    # TEST 3
    test_query(graph_runner, "What is the capital of France?")
    
    # TEST 4 (Hallucination / Unknown Question Test)
    test_query(graph_runner, "What is the population of Japan?")
    
    print("========================================")
    print("LANGGRAPH TEST COMPLETE")
    print("========================================")

if __name__ == "__main__":
    main()
