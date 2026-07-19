import pandas as pd
from pathlib import Path


class RiskScoring:
    """
    Risk Analysis Module
    Project FORESIGHT
    """

    def __init__(self):

        self.base = Path(__file__).resolve().parents[2]

        self.inventory = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "inventory_optimization.csv"
        )

    # =====================================================
    # Calculate Risk Score
    # =====================================================

    def calculate_risk(self):

        df = self.inventory.copy()

        risk_scores = []
        risk_levels = []
        recommendations = []

        for _, row in df.iterrows():

            stock = row["Current_Stock"]

            reorder = row["Reorder_Point"]

            safety = row["Safety_Stock"]

            demand = row["Average_Daily_Demand"]

            status = row["Inventory_Status"]

            # ------------------------------------------
            # LOW STOCK
            # ------------------------------------------

            if status == "Low Stock":

                score = 90

                level = "High"

                recommendation = (
                    "Urgent reorder required to avoid stock-out."
                )

            # ------------------------------------------
            # OVER STOCK
            # ------------------------------------------

            elif status == "Over Stock":

                excess = stock - row["EOQ"]

                score = min(
                    80,
                    50 + excess / 5
                )

                level = "Medium"

                recommendation = (
                    "Reduce inventory or increase promotional sales."
                )

            # ------------------------------------------
            # NORMAL
            # ------------------------------------------

            else:

                if demand > 10:

                    score = 35

                    level = "Low"

                    recommendation = (
                        "Monitor demand regularly."
                    )

                else:

                    score = 15

                    level = "Very Low"

                    recommendation = (
                        "Inventory level is healthy."
                    )

            risk_scores.append(round(score, 2))
            risk_levels.append(level)
            recommendations.append(recommendation)

        df["Risk_Score"] = risk_scores

        df["Risk_Level"] = risk_levels

        df["Recommendation"] = recommendations

        return df

    # =====================================================
    # Risk Summary
    # =====================================================

    def risk_summary(self, df):

        print("\n==============================")

        print("Risk Level Summary")

        print("==============================")

        print(df["Risk_Level"].value_counts())

        print("\nAverage Risk Score")

        print(round(df["Risk_Score"].mean(), 2))

    # =====================================================
    # Save Result
    # =====================================================

    def save(self):

        result = self.calculate_risk()

        output = (
            self.base /
            "data" /
            "processed" /
            "risk_analysis.csv"
        )

        result.to_csv(
            output,
            index=False
        )

        print("\n======================================")

        print("Risk Analysis Completed Successfully")

        print("======================================")

        print("\nSaved File")

        print(output)

        self.risk_summary(result)

        print("\nPreview")

        print(result.head())


if __name__ == "__main__":

    risk = RiskScoring()

    risk.save()