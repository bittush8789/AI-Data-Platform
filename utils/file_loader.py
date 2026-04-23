import pandas as pd
import json
import os
import re
from typing import Union, List, Dict

class FileLoader:
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @staticmethod
    def load_excel(file_path: str, sheet_name: Union[str, int, None] = 0) -> pd.DataFrame:
        return pd.read_excel(file_path, sheet_name=sheet_name)

    @staticmethod
    def load_json(file_path: str) -> pd.DataFrame:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Logic to flatten nested JSON
        if isinstance(data, list):
            return pd.json_normalize(data)
        elif isinstance(data, dict):
            # Check if there's a main key with a list of objects
            for key, value in data.items():
                if isinstance(value, list):
                    return pd.json_normalize(value)
            return pd.json_normalize([data])
        return pd.DataFrame()

    @staticmethod
    def load_log(file_path: str) -> pd.DataFrame:
        """Parses common log formats into a DataFrame."""
        logs = []
        # Common Regex for Nginx/Apache logs
        log_pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp>.*?)\]\s+"(?P<method>\w+)\s+(?P<path>.*?)\s+HTTP\/.*?"\s+(?P<status>\d+)\s+(?P<size>\d+)'
        )
        
        with open(file_path, 'r') as f:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    logs.append(match.groupdict())
                else:
                    # Fallback: simple line splitting if regex fails
                    logs.append({"raw_log": line.strip()})
        
        return pd.DataFrame(logs)

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        return os.path.splitext(file_path)[1].lower()
