from utils.file_loader import FileLoader
import pandas as pd

class FileAgent:
    def __init__(self):
        self.loader = FileLoader()

    def load_any_file(self, file_path: str):
        ext = self.loader.get_file_extension(file_path)
        if ext == '.csv':
            return self.loader.load_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self.loader.load_excel(file_path)
        elif ext == '.json':
            return self.loader.load_json(file_path)
        elif ext in ['.log', '.txt']:
            return self.loader.load_log(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
