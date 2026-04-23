from agents.base_agent import BaseAgent
import pandas as pd

class SchemaAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def understand_schema(self, df: pd.DataFrame):
        schema = {
            "columns": df.columns.tolist(),
            "types": df.dtypes.astype(str).to_dict(),
            "sample": df.head(2).to_dict()
        }
        
        system_prompt = "You are a Database Architect. Explain the schema and the likely purpose of this dataset."
        return self.call_llm(system_prompt, str(schema))
