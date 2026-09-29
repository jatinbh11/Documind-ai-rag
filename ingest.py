import os
from src.config import PDF_PATH
from src.ingestion import load_pdf, create_chunks

def main():
    print("========================================")
    print("PDF INGESTION")
    print("=============\n")
    print(f"PDF:\n{PDF_PATH}\n")
    
    try:
        # 1. Load PDF
        total_pages, documents = load_pdf(PDF_PATH)
        
        print(f"Pages found: {total_pages}")
        print(f"Pages with text: {len(documents)}")
        
        # 2. Create chunks
        chunks = create_chunks(documents)
        print(f"\nTotal chunks: {len(chunks)}\n")
        
        # 3. Display sample chunks
        for i in range(min(3, len(chunks))):
            chunk = chunks[i]
            metadata = chunk["metadata"]
            text = chunk["text"]
            
            print("========================================")
            print(f"SAMPLE CHUNK {i+1}")
            print("==============\n")
            
            print("Chunk ID:")
            print(metadata['chunk_id'], "\n")
            
            print("Source:")
            print(metadata['source'], "\n")
            
            print("Page:")
            print(metadata['page'], "\n")
            
            print("Character count:")
            print(len(text), "\n")
            
            # Print truncated text safely
            display_text = text if len(text) <= 250 else text[:250] + "..."
            print("Text:")
            print(display_text, "\n")
            
        print("========================================")
        print("INGESTION COMPLETE")
        print("==================\n")
        
    except FileNotFoundError:
        print("========================================")
        print("ERROR")
        print("=====\n")
        print(f"Missing PDF: Please place agentic-ai.pdf inside data/\n")
    except Exception as e:
        print("========================================")
        print("ERROR")
        print("=====\n")
        print(f"Failed during ingestion: {str(e)}\n")

if __name__ == "__main__":
    main()
