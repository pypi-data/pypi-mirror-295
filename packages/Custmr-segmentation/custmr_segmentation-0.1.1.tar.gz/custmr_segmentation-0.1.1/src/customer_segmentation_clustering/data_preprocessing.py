# data_preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate_structure(self, required_columns: dict) -> bool:
        """
        Validate the structure of the dataframe.

        Parameters:
        - required_columns (dict): Dictionary with column names as keys and data types as values.

        Returns:
        - bool: True if the dataframe meets the structure requirements, else False.
        """
        for column, dtype in required_columns.items():
            if column not in self.df.columns:
                print(f"Missing column: {column}")
                return False
            if column == 'InvoiceDate':
                self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], errors='coerce')
                if self.df['InvoiceDate'].isnull().all():
                    print("Column 'InvoiceDate' conversion to datetime failed.")
                    return False
            elif not pd.api.types.is_dtype_equal(self.df[column].dtype, dtype):
                print(f"Column {column} has incorrect type. Expected {dtype}, got {self.df[column].dtype}.")
                return False
        return True

    def remove_nulls(self, strategy: str = 'mode') -> pd.DataFrame:
        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy in ['mean', 'median', 'mode']:
            for column in self.df.select_dtypes(include=['object', 'number']).columns:
                if self.df[column].isnull().any():
                    if strategy == 'mode':
                        mode_val = self.df[column].mode()
                        if not mode_val.empty:
                            self.df[column] = self.df[column].fillna(mode_val.iloc[0])
                        else:
                            print(f"No mode found for column '{column}'. Skipping imputation.")
                    elif strategy == 'mean':
                        self.df[column] = self.df[column].fillna(self.df[column].mean())
                    elif strategy == 'median':
                        self.df[column] = self.df[column].fillna(self.df[column].median())
        else:
            raise ValueError("Invalid strategy. Use 'drop', 'mean', 'median', or 'mode'.")
        return self.df

    def remove_outliers(self, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    # Handle Non-Numeric Values
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df = self.df[~self.df[col].astype(str).str.contains('[^0-9.]', na=False)]

        if method == 'zscore':
            from scipy.stats import zscore
            z_scores = np.abs(zscore(self.df.select_dtypes(include=[np.number])))
            self.df = self.df[(z_scores < threshold).all(axis=1)]
        elif method == 'iqr':
            # Calculate IQR
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            Q1 = self.df[numeric_cols].quantile(0.25)
            Q3 = self.df[numeric_cols].quantile(0.75)
            IQR = Q3 - Q1

            # Filter Outliers Based on IQR
            self.df = self.df[~((self.df[numeric_cols] < (Q1 - threshold * IQR)) | (self.df[numeric_cols] > (Q3 + threshold * IQR))).any(axis=1)]
        else:
            raise ValueError("Invalid method. Use 'zscore' or 'iqr'.")
        return self.df
    def scale_data(self, method: str = 'standard') -> pd.DataFrame:
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Invalid method. Use 'standard' or 'minmax'.")

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        scaled_values = scaler.fit_transform(self.df[numeric_cols])

        for col, dtype in zip(numeric_cols, self.df[numeric_cols].dtypes):
            self.df[col] = scaled_values[:, numeric_cols.get_loc(col)].astype(dtype)
            
        return self.df
