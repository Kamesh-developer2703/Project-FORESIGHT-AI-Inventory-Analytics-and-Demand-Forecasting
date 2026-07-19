import pandas as pd
from pathlib import Path


class DataLoader:
    """
    Data Loader for Project FORESIGHT

    Loads the retail_sales.csv dataset and performs
    basic validation.
    """

    def __init__(self, data_path="../../data/raw"):
        self.base_path = Path(__file__).resolve().parent / data_path

    # ======================================================
    # Load Retail Sales Dataset
    # ======================================================

    def load_retail_sales(self):
        """
        Load retail_sales.csv
        """

        path = self.base_path / "retail_sales.csv"

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found:\n{path}"
            )

        df = pd.read_csv(path)

        print("✅ retail_sales.csv Loaded Successfully")
        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")

        return df

    # ======================================================
    # Validate Dataset
    # ======================================================

    def validate_dataset(self, df):
        """
        Validate required columns.
        """

        required_columns = [
    "Transaction ID",
    "Date",
    "Customer ID",
    "Gender",
    "Age",
    "Product Category",
    "Quantity",
    "Price per Unit",
    "Total Amount"
]

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        print("✅ Dataset Validation Successful")

        return True

    # ======================================================
    # Data Summary
    # ======================================================

    def dataset_summary(self, df):
        """
        Print dataset information.
        """

        print("\n========== DATA SUMMARY ==========")

        print(f"Rows       : {len(df)}")
        print(f"Columns    : {len(df.columns)}")

        print("\nColumn Names")

        print(df.columns.tolist())

        print("\nMissing Values")

        print(df.isnull().sum())

        print("\nData Types")

        print(df.dtypes)

        print("\nFirst Five Records")

        print(df.head())

    # ======================================================
    # Load Complete Dataset
    # ======================================================

    def load_data(self):
        """
        Load and validate dataset.
        """

        df = self.load_retail_sales()

        self.validate_dataset(df)

        return df


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    loader = DataLoader()

    sales_df = loader.load_data()

    loader.dataset_summary(sales_df)