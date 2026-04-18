import os
from openai import OpenAI
from dotenv import load_dotenv
from backend.app.core.embedding_model import EMBEDDING_MODEL, EMBEDDING_DIMENSION

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):
        text = text.replace("\n", " ")
        
        response = client.embeddings.create(
            input=[text],
            model=EMBEDDING_MODEL,
            dimensions=EMBEDDING_DIMENSION
        )
        
        return response.data[0].embedding


