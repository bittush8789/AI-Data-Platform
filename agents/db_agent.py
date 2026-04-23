from utils.db_connector import DBConnector
import pandas as pd

class DBAgent:
    def __init__(self, db_type: str, config: dict):
        self.connector = DBConnector(db_type, config)

    def get_data(self, table_name: str):
        query = f"SELECT * FROM {table_name}"
        return self.connector.execute_query(query)

    def list_tables(self):
        return self.connector.get_table_names()
