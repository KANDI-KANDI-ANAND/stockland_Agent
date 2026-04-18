import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMClient:

    @staticmethod
    async def generate_answer(prompt: str):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        answer = response.choices[0].message.content
        
        print("\n===== OPENAI RESPONSE =====")
        print(answer)
        print("===========================\n")
        
        return answer
