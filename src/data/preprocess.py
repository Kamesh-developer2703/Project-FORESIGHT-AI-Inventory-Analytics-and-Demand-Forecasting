import pandas as pd
from pathlib import Path
from data_loader import DataLoader


class DataPreprocessor:
    """
    Data Preprocessing Module
    Project FORESIGHT
    """

    def __init__(self):
        self.loader = DataLoader()

    # ======================================================
    # Load Dataset
    # ======================================================

    def load_data(self):
        return self.loader.load_data()

    # ======================================================
    # Remove Duplicates
    # ======================================================

    def remove_duplicates(self, df):

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        print(f"✅ Removed {before-after} duplicate rows")

        return df

    # ======================================================
    # Handle Missing Values
    # ======================================================

    def handle_missing_values(self, df):

        print("\nMissing Values Before Cleaning")

        print(df.isnull().sum())

        df["Gender"] = df["Gender"].fillna("Unknown")

        df["Product Category"] = df["Product Category"].fillna("Unknown")

        df["Quantity"] = df["Quantity"].fillna(0)

        df["Price per Unit"] = df["Price per Unit"].fillna(
            df["Price per Unit"].median()
        )

        df["Total Amount"] = df["Total Amount"].fillna(
            df["Total Amount"].median()
        )

        print("\nMissing Values After Cleaning")

        print(df.isnull().sum())

        return df

    # ======================================================
    # Convert Date
    # ======================================================

    def convert_date(self, df):

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    # ======================================================
    # Standardize Text
    # ======================================================

    def clean_text_columns(self, df):

        df["Gender"] = df["Gender"].str.strip().str.title()

        df["Product Category"] = (
            df["Product Category"]
            .str.strip()
            .str.title()
        )

        return df

    # ======================================================
    # Feature Creation
    # ======================================================

    def create_datetime_features(self, df):

        df["Year"] = df["Date"].dt.year

        df["Month"] = df["Date"].dt.month

        df["Day"] = df["Date"].dt.day

        df["DayOfWeek"] = df["Date"].dt.day_name()

        df["Quarter"] = df["Date"].dt.quarter

        return df

    # ======================================================
    # Verify Total Amount
    # ======================================================

    def verify_total_amount(self, df):

        df["Calculated Total"] = (
            df["Quantity"] *
            df["Price per Unit"]
        )

        return df

    # ======================================================
    # Save Processed Dataset
    # ======================================================

    def save_processed_data(self):

        processed_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "processed"
        )

        processed_path.mkdir(
            parents=True,
            exist_ok=True
        )

        df = self.load_data()

        df = self.remove_duplicates(df)

        df = self.handle_missing_values(df)

        df = self.convert_date(df)

        df = self.clean_text_columns(df)

        df = self.create_datetime_features(df)

        df = self.verify_total_amount(df)

        output_file = processed_path / "processed_retail_sales.csv"

        df.to_csv(
            output_file,
            index=False
        )

        print("\n===================================")

        print("✅ Data Preprocessing Completed")

        print(f"Saved To : {output_file}")

        print("===================================")

        return df


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    processor = DataPreprocessor()

    df = processor.save_processed_data()

    print("\nProcessed Dataset")

    print(df.head())