import pandas as pd

class Validator:
    @staticmethod
    def validate_df(df: pd.DataFrame):
        report = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_count": df.duplicated().sum(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        return report

    @staticmethod
    def check_empty(df: pd.DataFrame):
        return df.empty
