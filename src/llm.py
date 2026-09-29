import requests
import logging
from src.config import OLLAMA_MODEL

logger = logging.getLogger(__name__)

class LocalLLM:
    """
    Wrapper for communicating with the local Ollama service.
    """
    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        
    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the local Ollama service and returns the generated text.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to local Ollama service: {e}")
            raise RuntimeError(f"Unable to connect to local Ollama service. Make sure Ollama is running. Error: {e}")
