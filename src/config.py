# src/config.py

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PDF Data path
PDF_PATH = os.path.join(BASE_DIR, "data", "agentic-ai.pdf")

# Chunking Configuration
# 1000 characters is approximately 200-250 words
CHUNK_SIZE = 1000

# 200 characters overlap ensures sentences aren't cleanly cut off at boundaries
CHUNK_OVERLAP = 200

# LLM Configuration
OLLAMA_MODEL = "llama3.2:3b"

# Vector Database Configuration
QDRANT_COLLECTION = "documind_agentic_ai"
