import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class LLMClient:

    BASE_URL = "https://openrouter.ai/api/v1"

    @staticmethod
    async def generate_answer(prompt: str):

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                f"{LLMClient.BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )

            data = response.json()

            print("\n===== LLM RESPONSE =====")
            print(data)
            print("========================\n")

            if "choices" not in data:
                raise Exception(f"OpenRouter API error: {data}")

            return data["choices"][0]["message"]["content"]