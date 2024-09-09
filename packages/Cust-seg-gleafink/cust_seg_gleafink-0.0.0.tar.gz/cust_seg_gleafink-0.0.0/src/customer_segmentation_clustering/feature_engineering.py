# feature_engineering.py

import pandas as pd
import numpy as np

class FeatureEngineering:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_rfm(self, customer_id: str, date_col: str, monetary_col: str) -> pd.DataFrame:
        """
        Calculate RFM (Recency, Frequency, Monetary) values.

        Parameters:
        - customer_id (str): Column name for customer ID.
        - date_col (str): Column name for transaction date.
        - monetary_col (str): Column name for monetary value.

        Returns:
        - pd.DataFrame: DataFrame with RFM values.
        """
        current_date = self.df[date_col].max()
        rfm = self.df.groupby(customer_id).agg({
            date_col: lambda x: (current_date - x.max()).days,
            customer_id: 'count',
            monetary_col: 'sum'
        }).rename(columns={date_col: 'Recency', customer_id: 'Frequency', monetary_col: 'Monetary'})
        return rfm

    def calculate_velocity(self, customer_id: str, date_col: str) -> pd.DataFrame:
        """
        Calculate velocity for each customer.

        Parameters:
        - customer_id (str): Column name for customer ID.
        - date_col (str): Column name for transaction date.

        Returns:
        - pd.DataFrame: DataFrame with velocity values.
        """
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        velocity = self.df.groupby(customer_id)[date_col].apply(
            lambda x: x.diff().mean().days).reset_index().rename(columns={date_col: 'Velocity'})
        return velocity

    def calculate_growth(self, customer_id: str, date_col: str, monetary_col: str) -> pd.DataFrame:
        """
        Calculate growth for each customer.

        Parameters:
        - customer_id (str): Column name for customer ID.
        - date_col (str): Column name for transaction date.
        - monetary_col (str): Column name for monetary value.

        Returns:
        - pd.DataFrame: DataFrame with growth values.
        """
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        growth = self.df.groupby(customer_id).apply(
            lambda x: (x[monetary_col].iloc[-1] - x[monetary_col].iloc[0]) / len(x)).reset_index().rename(columns={0: 'Growth'})
        return growth

