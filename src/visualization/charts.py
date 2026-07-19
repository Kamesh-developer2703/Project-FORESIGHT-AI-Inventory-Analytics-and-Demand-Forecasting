import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path


class Visualization:

    def __init__(self):

        self.base = Path(__file__).resolve().parents[2]

        self.figure_path = (
            self.base /
            "reports" /
            "figures"
        )

        self.figure_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------
        # Load Processed Files
        # --------------------------------------------

        self.sales = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "processed_retail_sales.csv"
        )

        self.inventory = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "inventory_optimization.csv"
        )

        self.risk = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "risk_analysis.csv"
        )

        self.forecast = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "forecast_results.csv"
        )

        self.model = joblib.load(
            self.base /
            "model" /
            "forecasting_model.pkl"
        )

        plt.style.use("ggplot")

        self.figsize = (10, 6)

        self.dpi = 120

    # =====================================================
    # Save Chart
    # =====================================================

    def save_chart(self, filename):

        plt.tight_layout()

        plt.savefig(
            self.figure_path / filename,
            dpi=self.dpi,
            bbox_inches="tight"
        )

        plt.close()

    # =====================================================
    # Daily Sales Trend
    # =====================================================

    def sales_trend(self):

        self.sales["Date"] = pd.to_datetime(
            self.sales["Date"]
        )

        trend = (

            self.sales

            .groupby("Date")["Quantity"]

            .sum()

        )

        plt.figure(figsize=self.figsize)

        plt.plot(

            trend.index,

            trend.values,

            linewidth=3,

            marker="o"

        )

        plt.title("Daily Sales Trend")

        plt.xlabel("Date")

        plt.ylabel("Quantity")

        plt.grid(True)

        self.save_chart("sales_trend.png")

    # =====================================================
    # Product Category Sales
    # =====================================================

    def category_sales(self):

        category = (

            self.sales

            .groupby("Product Category")["Quantity"]

            .sum()

            .sort_values()

        )

        plt.figure(figsize=self.figsize)

        plt.barh(

            category.index,

            category.values

        )

        plt.title("Product Category Sales")

        plt.xlabel("Quantity Sold")

        self.save_chart("category_sales.png")

    # =====================================================
    # Revenue by Category
    # =====================================================

    def revenue_chart(self):

        revenue = (

            self.sales

            .groupby("Product Category")["Total Amount"]

            .sum()

            .sort_values()

        )

        plt.figure(figsize=self.figsize)

        plt.bar(

            revenue.index,

            revenue.values

        )

        plt.title("Revenue by Category")

        plt.ylabel("Revenue")

        plt.xticks(rotation=20)

        self.save_chart("revenue.png")

    # =====================================================
    # Inventory Dashboard
    # =====================================================

    def inventory_chart(self):

        plt.figure(figsize=self.figsize)

        plt.bar(

            self.inventory["Product_Category"],

            self.inventory["Current_Stock"]

        )

        plt.title("Current Stock")

        plt.ylabel("Stock")

        plt.xticks(rotation=20)

        self.save_chart("inventory.png")

    # =====================================================
    # EOQ Chart
    # =====================================================

    def eoq_chart(self):

        plt.figure(figsize=self.figsize)

        plt.bar(

            self.inventory["Product_Category"],

            self.inventory["EOQ"]

        )

        plt.title("Economic Order Quantity")

        plt.ylabel("EOQ")

        plt.xticks(rotation=20)

        self.save_chart("eoq.png")

    # =====================================================
    # Forecast Chart
    # =====================================================

    def forecast_chart(self):

        plt.figure(figsize=self.figsize)

        plt.plot(

            self.forecast["Actual"],

            marker="o",

            label="Actual"

        )

        plt.plot(

            self.forecast["Predicted"],

            marker="s",

            linestyle="--",

            label="Predicted"

        )

        plt.legend()

        plt.grid(True)

        plt.title("Demand Forecast")

        self.save_chart("forecast.png")

    # =====================================================
    # Feature Importance
    # =====================================================

    def feature_importance(self):

        features = [

            "Age",

            "Gender",

            "Product Category",

            "Price per Unit",

            "Year",

            "Month",

            "Day",

            "Quarter"

        ]

        importance = pd.DataFrame({

            "Feature": features,

            "Importance": self.model.feature_importances_

        })

        importance = importance.sort_values(

            by="Importance",

            ascending=True

        )

        plt.figure(figsize=self.figsize)

        plt.barh(

            importance["Feature"],

            importance["Importance"]

        )

        plt.title("Feature Importance")

        self.save_chart("feature_importance.png")

    # =====================================================
    # Risk Distribution
    # =====================================================

    def risk_distribution(self):

        risk = self.risk["Risk_Level"].value_counts()

        plt.figure(figsize=(8, 6))

        plt.pie(

            risk.values,

            labels=risk.index,

            autopct="%1.1f%%"

        )

        plt.title("Risk Distribution")

        self.save_chart("risk_distribution.png")

    # =====================================================
    # Generate All
    # =====================================================

    def generate_all(self):

        print("\nGenerating Charts...\n")

        self.sales_trend()

        self.category_sales()

        self.revenue_chart()

        self.inventory_chart()

        self.eoq_chart()

        self.forecast_chart()

        self.feature_importance()

        self.risk_distribution()

        print("All Charts Generated Successfully")

        print(self.figure_path)


if __name__ == "__main__":

    Visualization().generate_all()