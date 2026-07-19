import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class DemandForecastModel:

    def __init__(self):

        self.base = Path(__file__).resolve().parents[2]

        self.data = pd.read_csv(
            self.base /
            "data" /
            "processed" /
            "processed_retail_sales.csv"
        )

        self.model = None

    # ---------------------------------------------------------
    # Prepare Dataset
    # ---------------------------------------------------------

    def prepare_data(self):

        df = self.data.copy()

        df["Date"] = pd.to_datetime(df["Date"])

        gender_encoder = LabelEncoder()
        category_encoder = LabelEncoder()

        df["Gender"] = gender_encoder.fit_transform(
            df["Gender"]
        )

        df["Product Category"] = category_encoder.fit_transform(
            df["Product Category"]
        )

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

        X = df[features]

        y = df["Quantity"]

        return train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )

    # ---------------------------------------------------------
    # Train Model
    # ---------------------------------------------------------

    def train(self):

        X_train, X_test, y_train, y_test = self.prepare_data()

        self.model = RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = (
            mean_squared_error(
                y_test,
                predictions
            ) ** 0.5
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        print("\n===================================")
        print("Demand Forecast Model")
        print("===================================")

        print(f"MAE  : {mae:.3f}")
        print(f"RMSE : {rmse:.3f}")
        print(f"R²   : {r2:.3f}")

        # ---------------------------------------------
        # Save Model
        # ---------------------------------------------

        model_path = self.base / "model"

        model_path.mkdir(
            exist_ok=True
        )

        joblib.dump(
            self.model,
            model_path / "forecasting_model.pkl"
        )

        # ---------------------------------------------
        # Save Forecast Results
        # ---------------------------------------------

        processed = (
            self.base /
            "data" /
            "processed"
        )

        pd.DataFrame({

            "Actual": y_test.values,

            "Predicted": predictions

        }).to_csv(

            processed /
            "forecast_results.csv",

            index=False

        )

        print("\nModel Saved Successfully")

        print(model_path / "forecasting_model.pkl")

        return self.model

    # ---------------------------------------------------------
    # Feature Importance
    # ---------------------------------------------------------

    def feature_importance(self):

        if self.model is None:

            self.model = joblib.load(
                self.base /
                "model" /
                "forecasting_model.pkl"
            )

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

        return importance.sort_values(
            by="Importance",
            ascending=False
        )


if __name__ == "__main__":

    forecast = DemandForecastModel()

    forecast.train()

    print("\nFeature Importance")

    print(forecast.feature_importance())