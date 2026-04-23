from agents.base_agent import BaseAgent

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def route_task(self, task_description: str):
        system_prompt = """
        You are the Supervisor Agent of a Multi-Agent Data Analyzer system.
        Your job is to route the user's request to the correct agent.
        Agents available:
        - CleaningAgent: For data cleaning, fixing nulls, duplicates.
        - KPIAgent: For detecting business metrics.
        - SQLAgent: For natural language to SQL conversion.
        - AnomalyAgent: For finding outliers or suspicious patterns.
        - InsightAgent: For explaining the data.
        - RecommendationAgent: For suggesting business actions.
        
        Respond ONLY with the name of the agent.
        """
        return self.call_llm(system_prompt, task_description)
