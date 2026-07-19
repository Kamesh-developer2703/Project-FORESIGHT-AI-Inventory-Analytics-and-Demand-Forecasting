import pandas as pd
import numpy as np
from pathlib import Path


class InventoryOptimizer:

    def __init__(self):

        self.base = Path(__file__).resolve().parents[2]

        self.sales = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "processed_retail_sales.csv"
        )

    # ---------------------------------------------------------
    # Prepare Inventory Dataset
    # ---------------------------------------------------------

    def prepare_inventory(self):

        df = self.sales.copy()

        inventory = (

            df.groupby("Product Category")

            .agg({

                "Quantity": "sum",

                "Price per Unit": "mean",

                "Total Amount": "sum"

            })

            .reset_index()

        )

        inventory.rename(

            columns={

                "Product Category": "Product_Category",

                "Quantity": "Total_Sales",

                "Price per Unit": "Price",

                "Total Amount": "Revenue"

            },

            inplace=True

        )

        return inventory

    # ---------------------------------------------------------
    # Inventory Optimization
    # ---------------------------------------------------------

    def optimize_inventory(self):

        inventory = self.prepare_inventory()

        inventory["Average_Daily_Demand"] = (

            inventory["Total_Sales"] / 365

        ).round(2)

        inventory["Lead_Time"] = 7

        inventory["Current_Stock"] = (

            inventory["Total_Sales"] * 0.25

        ).round().astype(int)

        inventory["Reorder_Point"] = (

            inventory["Average_Daily_Demand"]

            * inventory["Lead_Time"]

        ).round(2)

        inventory["Safety_Stock"] = (

            inventory["Average_Daily_Demand"] * 3

        ).round(2)

        ordering_cost = 100

        holding_cost = 10

        annual_demand = inventory["Average_Daily_Demand"] * 365

        inventory["EOQ"] = np.sqrt(

            (2 * annual_demand * ordering_cost)

            / holding_cost

        ).round(2)

        # -----------------------------------------
        # Inventory Status
        # -----------------------------------------

        status = []

        for _, row in inventory.iterrows():

            if row["Current_Stock"] <= row["Reorder_Point"]:

                status.append("Low Stock")

            elif row["Current_Stock"] >= row["EOQ"]:

                status.append("Over Stock")

            else:

                status.append("Normal")

        inventory["Inventory_Status"] = status

        return inventory

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(self):

        inventory = self.optimize_inventory()

        output = (

            self.base /

            "data" /

            "processed" /

            "inventory_optimization.csv"

        )

        inventory.to_csv(

            output,

            index=False

        )

        print("\n====================================")

        print("Inventory Optimization Completed")

        print("====================================")

        print("\nSaved File")

        print(output)

        print("\nInventory Status")

        print(

            inventory["Inventory_Status"]

            .value_counts()

        )

        print("\nPreview")

        print(inventory.head())


if __name__ == "__main__":

    optimizer = InventoryOptimizer()

    optimizer.save()