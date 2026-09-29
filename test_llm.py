import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.llm import LocalLLM

def main():
    print("========================================")
    print("OLLAMA TEST")
    print("========================================")
    
    try:
        llm = LocalLLM()
        print(f"\nModel:\n{llm.model}\n")
        
        response = llm.generate("Say hello in one word.")
        print("Status:\nCONNECTED\n")
        print(f"Response:\n{response}\n")
    except Exception as e:
        print("Status:\nFAILED\n")
        print(f"Error:\n{e}\n")
        
    print("OLLAMA TEST COMPLETE")
    print("========================================\n")

if __name__ == "__main__":
    main()
