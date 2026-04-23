import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from agents.base_agent import BaseAgent

class AnomalyAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def detect_anomalies(self, df: pd.DataFrame):
        results = []
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return pd.DataFrame(), "No numeric columns for anomaly detection."

        # Method 1: Isolation Forest
        model = IsolationForest(contamination=0.05, random_state=42)
        # Drop rows with NaN for the model
        df_clean = df[numeric_cols].dropna()
        if len(df_clean) > 0:
            preds = model.fit_predict(df_clean)
            anomalies = df_clean[preds == -1]
            results.append(anomalies)

        # Method 2: Z-Score
        z_anomalies = []
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                outliers = df[(df[col] - mean).abs() > 3 * std]
                if not outliers.empty:
                    z_anomalies.append(outliers)
        
        final_anomalies = pd.concat(results + z_anomalies).drop_duplicates()
        return final_anomalies, f"Detected {len(final_anomalies)} potential anomalies."

    def explain_anomalies(self, anomaly_summary: str):
        system_prompt = "You are a Security and Fraud Analyst. Explain why these data points might be considered anomalies."
        return self.call_llm(system_prompt, anomaly_summary)
