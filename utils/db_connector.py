import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
import os
from typing import Optional, Dict, Any

class DBConnector:
    def __init__(self, db_type: str = "sqlite", config: Optional[Dict[str, Any]] = None):
        self.db_type = db_type
        self.config = config
        self.engine = None
        self._initialize_engine()

    def _initialize_engine(self):
        if self.db_type == "sqlite":
            db_path = self.config.get("path", "database/app_data.db") if self.config else "database/app_data.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.engine = create_engine(f"sqlite:///{db_path}")
        elif self.db_type == "postgresql":
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host")
            port = self.config.get("port", 5432)
            database = self.config.get("database")
            self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
        elif self.db_type == "mysql":
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host")
            port = self.config.get("port", 3306)
            database = self.config.get("database")
            self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

    def execute_query(self, query: str):
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            if result.returns_rows:
                return pd.DataFrame(result.fetchall(), columns=result.keys())
            connection.commit()
            return None

    def get_table_names(self):
        with self.engine.connect() as connection:
            if self.db_type == "sqlite":
                query = "SELECT name FROM sqlite_master WHERE type='table';"
            else:
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            df = pd.read_sql(query, connection)
            return df.iloc[:, 0].tolist()

    def get_table_schema(self, table_name: str):
        return pd.read_sql(f"SELECT * FROM {table_name} LIMIT 0", self.engine).columns.tolist()

    def save_to_internal_db(self, table_name: str, df: pd.DataFrame, if_exists: str = "append"):
        # This is for the app's internal SQLite
        internal_engine = create_engine("sqlite:///database/app_data.db")
        df.to_sql(table_name, internal_engine, if_exists=if_exists, index=False)
