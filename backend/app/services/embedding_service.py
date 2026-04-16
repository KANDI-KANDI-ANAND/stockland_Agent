import os
from dotenv import load_dotenv

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

from backend.app.core.embedding_model import model

class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):
        embedding = model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
