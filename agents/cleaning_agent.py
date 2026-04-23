import pandas as pd
import numpy as np
from agents.base_agent import BaseAgent

class CleaningAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def clean_data(self, df: pd.DataFrame):
        summary = []
        
        # 1. Remove Duplicates
        dup_count = df.duplicated().sum()
        df = df.drop_duplicates()
        if dup_count > 0:
            summary.append(f"Removed {dup_count} duplicate rows.")

        # 2. Handle Null Values
        # For numeric, fill with mean. For categorical, fill with mode.
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                    summary.append(f"Filled {null_count} nulls in '{col}' with mean.")
                else:
                    df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
                    summary.append(f"Filled {null_count} nulls in '{col}' with mode/Unknown.")

        # 3. Standardize Text (Strip and Lowercase for object columns)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            # Standardize casing to Title Case for better presentation
            df[col] = df[col].str.title()
        
        # 4. Fix Column Names
        df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]
        
        return df, summary

    def get_ai_cleaning_suggestions(self, df_head: str):
        system_prompt = "You are a Data Cleaning Expert. Analyze the following data sample and suggest cleaning steps."
        return self.call_llm(system_prompt, f"Data Sample (First 5 rows):\n{df_head}")
