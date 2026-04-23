import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=self.api_key)

    def call_llm(self, system_prompt: str, user_prompt: str, model: str = "llama-3.3-70b-versatile"):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=model,
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
