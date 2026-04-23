import sqlparse
import sqlite3
import pandas as pd
import re

class SQLParser:
    def __init__(self, sql_content: str):
        self.sql_content = sql_content

    def parse_and_rebuild(self, db_path: str = ":memory:"):
        """Executes SQL script into a temporary or in-memory SQLite DB and returns table names."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Split by semicolon but ignore inside quotes
        statements = sqlparse.split(self.sql_content)
        
        table_names = []
        for statement in statements:
            if not statement.strip():
                continue
            
            # Basic table extraction for tracking
            create_match = re.search(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_0-9]+)", statement, re.IGNORECASE)
            if create_match:
                table_names.append(create_match.group(1))
            
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Error executing statement: {e}")
        
        conn.commit()
        return conn, table_names

    @staticmethod
    def get_df_from_table(conn, table_name):
        return pd.read_sql(f"SELECT * FROM {table_name}", conn)
