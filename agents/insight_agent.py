from agents.base_agent import BaseAgent

class InsightAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def generate_insights(self, data_summary: str):
        system_prompt = "You are a Data Scientist. Provide deep insights and trends based on the data summary provided."
        return self.call_llm(system_prompt, data_summary)
