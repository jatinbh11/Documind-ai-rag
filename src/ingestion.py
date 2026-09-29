import os
import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_pdf(file_path: str) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Loads a PDF file and extracts text page by page.
    Returns:
        Tuple containing (total_pages, list_of_extracted_documents)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    documents = []
    try:
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text("text").strip()
            
            # Safely ignore completely empty pages
            if text:
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": page_num + 1  # 1-indexed for human readability
                    }
                })
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {str(e)}")
        
    if not documents:
        raise ValueError("No extractable text found in the PDF. It may be an image-only PDF.")
        
    return total_pages, documents

def create_chunks(documents: List[Dict[str, Any]], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Dict[str, Any]]:
    """
    Splits document text into smaller chunks while preserving metadata.
    """
    if not documents:
        raise ValueError("Empty documents list provided for chunking.")

    # This splitter intelligently tries to split by paragraphs, then sentences.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []
    chunk_counter = 1

    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]
        
        split_texts = text_splitter.split_text(text)
        
        for piece in split_texts:
            if not piece.strip():
                continue # Skip empty chunks
                
            chunks.append({
                "text": piece,
                "metadata": {
                    "source": metadata["source"],
                    "page": metadata["page"],
                    "chunk_id": f"chunk_{chunk_counter:04d}"
                }
            })
            chunk_counter += 1
            
    if not chunks:
        raise ValueError("No chunks were created from the provided documents.")
        
    return chunks
