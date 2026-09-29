import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def main():
    print("========================================")
    print("FASTAPI TEST")
    print("========================================\n")

    # TEST 1
    response = client.get("/")
    print("GET /")
    print(f"Status: {response.status_code}")
    print("PASS" if response.status_code == 200 else "FAIL")
    print()
    
    # TEST 2
    response = client.get("/health")
    print("GET /health")
    print(f"Status: {response.status_code}")
    print("PASS" if response.status_code == 200 else "FAIL")
    print()
    
    # TEST 3
    response = client.post("/ask", json={"question": "What is Agentic AI?"})
    data = response.json()
    print("POST /ask")
    print("Question: What is Agentic AI?")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"RAG Status: {data.get('status')}")
        print(f"Retrieved Chunks: {len(data.get('retrieved_context', []))}")
        print(f"Retrieval Score: {data.get('retrieval_score')}")
    print("PASS" if response.status_code == 200 and data.get("status") == "success" and len(data.get("retrieved_context", [])) > 0 and data.get("retrieval_score") is not None and data.get("answer") else "FAIL")
    print()

    # TEST 4
    response = client.post("/ask", json={"question": "What are AI agents?"})
    data = response.json()
    print("POST /ask")
    print("Question: What are AI agents?")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"RAG Status: {data.get('status')}")
        print(f"Retrieved Chunks: {len(data.get('retrieved_context', []))}")
    print("PASS" if response.status_code == 200 and data.get("status") == "success" and len(data.get("retrieved_context", [])) > 0 else "FAIL")
    print()
    
    # TEST 5
    response = client.post("/ask", json={"question": "What is the capital of France?"})
    data = response.json()
    print("POST /ask")
    print("Question: What is the capital of France?")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"RAG Status: {data.get('status')}")
        print(f"Retrieved Chunks: {len(data.get('retrieved_context', []))}")
    print("PASS" if response.status_code == 200 and data.get("status") == "no_context" and len(data.get("retrieved_context", [])) == 0 and data.get("retrieval_score") is None and data.get("answer") == "The answer is not available in the provided knowledge base." else "FAIL")
    print()

    # TEST 6
    response = client.post("/ask", json={"question": "What is the population of Japan?"})
    data = response.json()
    print("POST /ask")
    print("Question: What is the population of Japan?")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"RAG Status: {data.get('status')}")
        print(f"Retrieved Chunks: {len(data.get('retrieved_context', []))}")
    print("PASS" if response.status_code == 200 and data.get("status") == "no_context" and len(data.get("retrieved_context", [])) == 0 else "FAIL")
    print()
    
    # TEST 7
    response = client.post("/ask", json={"question": "   "})
    print("Empty question:")
    print(f"Status: {response.status_code}")
    print("PASS" if response.status_code in [422, 400] else "FAIL")
    print()
    
    print("========================================")
    print("FASTAPI TEST COMPLETE")
    print("========================================")

if __name__ == "__main__":
    main()
