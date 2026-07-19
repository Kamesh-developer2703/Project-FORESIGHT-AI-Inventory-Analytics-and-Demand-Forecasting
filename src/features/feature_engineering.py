import pandas as pd
from pathlib import Path


class FeatureEngineering:

    def __init__(self):
        base = Path(__file__).resolve().parents[2]

        self.sales = pd.read_csv(
            base / "data" / "processed" / "cleaned_sales.csv"
        )

        self.inventory = pd.read_csv(
            base / "data" / "processed" / "cleaned_inventory.csv"
        )

    def create_time_features(self):

        self.sales["Sale_Date"] = pd.to_datetime(self.sales["Sale_Date"])

        self.sales["Year"] = self.sales["Sale_Date"].dt.year
        self.sales["Month"] = self.sales["Sale_Date"].dt.month
        self.sales["Day"] = self.sales["Sale_Date"].dt.day
        self.sales["DayOfWeek"] = self.sales["Sale_Date"].dt.day_name()

        return self.sales

    def create_lag_features(self):

        self.sales = self.sales.sort_values("Sale_Date")

        self.sales["Previous_Day_Sales"] = self.sales["Quantity"].shift(1)

        self.sales["Previous_Day_Sales"] = self.sales[
            "Previous_Day_Sales"
        ].fillna(0)

        return self.sales

    def create_rolling_average(self):

        self.sales["Rolling_Avg_7"] = (
            self.sales["Quantity"]
            .rolling(window=7, min_periods=1)
            .mean()
        )

        return self.sales

    def calculate_inventory_value(self):

        self.inventory["Inventory_Value"] = (
            self.inventory["Stock"] *
            self.inventory["Price"]
        )

        return self.inventory

    def save_features(self):

        processed = Path(__file__).resolve().parents[2] / "data" / "processed"

        self.create_time_features()
        self.create_lag_features()
        self.create_rolling_average()
        self.calculate_inventory_value()

        self.sales.to_csv(
            processed / "sales_features.csv",
            index=False
        )

        self.inventory.to_csv(
            processed / "inventory_features.csv",
            index=False
        )

        print("✅ Feature Engineering Completed Successfully")


if __name__ == "__main__":

    feature = FeatureEngineering()

    feature.save_features()