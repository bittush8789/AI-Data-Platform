from agents.base_agent import BaseAgent
import pandas as pd
import json

class KPIAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def detect_kpis(self, df: pd.DataFrame):
        columns = df.columns.tolist()
        sample_data = df.head(3).to_dict()
        
        system_prompt = """
        You are a Business Intelligence expert. Identify the most relevant KPIs (Key Performance Indicators) from the provided column names and sample data.
        Categorize them into Sales, Finance, Marketing, HR, or Logs.
        Return the result as a JSON object with the following structure:
        {
            "kpis": [
                {"name": "Revenue", "column": "total_price", "category": "Sales", "aggregation": "sum"},
                ...
            ]
        }
        Respond ONLY with the JSON.
        """
        
        user_prompt = f"Columns: {columns}\nSample Data: {sample_data}"
        response = self.call_llm(system_prompt, user_prompt)
        
        try:
            # Clean response to handle potential markdown
            clean_response = response.strip().strip('`').replace('json', '')
            kpi_data = json.loads(clean_response)
            return kpi_data.get("kpis", [])
        except Exception as e:
            print(f"Error parsing KPI response: {e}")
            return []

    def calculate_kpi_values(self, df: pd.DataFrame, kpis: list):
        results = {}
        for kpi in kpis:
            col = kpi['column']
            agg = kpi['aggregation']
            name = kpi['name']
            
            if col in df.columns:
                if agg == "sum":
                    results[name] = df[col].sum()
                elif agg == "mean":
                    results[name] = df[col].mean()
                elif agg == "count":
                    results[name] = df[col].count()
        return results
