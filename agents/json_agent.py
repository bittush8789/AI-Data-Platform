from agents.base_agent import BaseAgent
from utils.file_loader import FileLoader

class JSONAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def process_json(self, file_path: str):
        df = FileLoader.load_json(file_path)
        system_prompt = "You are a JSON parsing expert. Explain how this nested data was flattened and its structure."
        explanation = self.call_llm(system_prompt, f"Columns after flattening: {df.columns.tolist()}")
        return df, explanation
