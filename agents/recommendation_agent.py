from agents.base_agent import BaseAgent

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def generate_recommendations(self, insight_summary: str):
        system_prompt = "You are a Business Strategist. Provide actionable recommendations based on the data insights."
        return self.call_llm(system_prompt, insight_summary)
