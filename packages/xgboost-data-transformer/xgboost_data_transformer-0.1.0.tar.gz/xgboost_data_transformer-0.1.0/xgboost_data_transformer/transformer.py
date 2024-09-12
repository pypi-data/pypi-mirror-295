# xgboost_data_transformer/transformer.py
import pandas as pd

class XGBoostDataTransformer:
    def __init__(self, drop_na=True):
        self.drop_na = drop_na

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the raw data for XGBoost:
        - Converts categorical variables to the appropriate format.
        - Removes missing values if drop_na is set to True.

        Parameters:
        data (pd.DataFrame): Raw input data.

        Returns:
        pd.DataFrame: Transformed data ready for XGBoost.
        """
        # Convert object columns to categorical
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].astype('category')

        # Remove missing values if specified
        if self.drop_na:
            data = data.dropna()

        return data
