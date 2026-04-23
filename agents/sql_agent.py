from agents.base_agent import BaseAgent

class SQLAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def generate_sql(self, question: str, schema_info: str, db_type: str = "sqlite"):
        system_prompt = f"""
        You are a SQL expert. Generate a {db_type} query to answer the user's question based on the provided schema.
        Return ONLY the SQL query code, no explanations.
        """
        
        user_prompt = f"Schema:\n{schema_info}\n\nQuestion: {question}"
        return self.call_llm(system_prompt, user_prompt)
