import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

from pathlib import Path

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = BASE_DIR / "model"

REPORT_DIR = BASE_DIR / "reports" / "figures"

# ==========================================================
# Custom CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background-color:#F8F9FA;
}

.block-container{
    padding-top:1rem;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.15);
}

h1,h2,h3{
    color:#1F4E79;
}

hr{
    margin-top:0.5rem;
    margin-bottom:1rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("📊 Project FORESIGHT")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Sales Analytics",

        "Demand Forecasting",

        "Inventory Analytics",

        "Risk Analysis"

    ]

)

st.sidebar.markdown("---")

st.sidebar.info(
"""
AI Powered Inventory Analytics

Demand Forecasting

Risk Analysis

Retail Business Dashboard
"""
)

# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_sales():

    return pd.read_csv(

        DATA_DIR /

        "processed_retail_sales.csv"

    )


@st.cache_data
def load_inventory():

    return pd.read_csv(

        DATA_DIR /

        "inventory_optimization.csv"

    )


@st.cache_data
def load_risk():

    return pd.read_csv(

        DATA_DIR /

        "risk_analysis.csv"

    )


@st.cache_data
def load_forecast():

    return pd.read_csv(

        DATA_DIR /

        "forecast_results.csv"

    )


@st.cache_resource
def load_model():

    return joblib.load(

        MODEL_DIR /

        "forecasting_model.pkl"

    )


# ==========================================================
# Load Everything
# ==========================================================

sales = load_sales()

inventory = load_inventory()

risk = load_risk()

forecast = load_forecast()

model = load_model()

# ==========================================================
# Helper Functions
# ==========================================================

def currency(value):

    return f"₹ {value:,.0f}"


def number(value):

    return f"{value:,.0f}"


# ==========================================================
# KPI Calculations
# ==========================================================

total_sales = sales["Total Amount"].sum()

total_quantity = sales["Quantity"].sum()

total_transactions = len(sales)

average_order = sales["Total Amount"].mean()

average_price = sales["Price per Unit"].mean()

unique_customers = sales["Customer ID"].nunique()

unique_categories = sales["Product Category"].nunique()

forecast_accuracy = (

    100

    -

    (

        abs(

            forecast["Actual"]

            -

            forecast["Predicted"]

        ).mean()

        /

        forecast["Actual"].mean()

    )

    *100

)

forecast_accuracy = round(

    forecast_accuracy,

    2

)

high_risk = len(

    risk[

        risk["Risk_Level"] == "High"

    ]

)

medium_risk = len(

    risk[

        risk["Risk_Level"] == "Medium"

    ]

)

low_risk = len(

    risk[

        risk["Risk_Level"].isin(

            [

                "Low",

                "Very Low"

            ]

        )

    ]

)

# ==========================================================
# Dashboard Title
# ==========================================================

st.title("📊 Project FORESIGHT")

st.caption(

    "AI Powered Inventory Analytics & Demand Forecasting Dashboard"

)

st.markdown("---")

# ==========================================================
# DASHBOARD
# ==========================================================

if page == "Dashboard":

    st.header("📈 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total Revenue",
            currency(total_sales)
        )

    with col2:
        st.metric(
            "🛒 Total Quantity Sold",
            number(total_quantity)
        )

    with col3:
        st.metric(
            "🧾 Transactions",
            number(total_transactions)
        )

    with col4:
        st.metric(
            "🎯 Forecast Accuracy",
            f"{forecast_accuracy}%"
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Customers",
            number(unique_customers)
        )

    with col2:
        st.metric(
            "📦 Product Categories",
            unique_categories
        )

    with col3:
        st.metric(
            "💵 Average Order",
            currency(average_order)
        )

    st.markdown("---")

    left, right = st.columns([2,1])

    with left:

        sales["Date"] = pd.to_datetime(sales["Date"])

        daily_sales = (

            sales

            .groupby("Date")["Total Amount"]

            .sum()

            .reset_index()

        )

        fig = px.line(

            daily_sales,

            x="Date",

            y="Total Amount",

            title="Daily Revenue Trend",

            markers=True

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        category = (

            sales

            .groupby("Product Category")["Total Amount"]

            .sum()

            .reset_index()

        )

        fig = px.pie(

            category,

            values="Total Amount",

            names="Product Category",

            hole=0.45,

            title="Revenue Share"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        gender = (

            sales["Gender"]

            .value_counts()

            .reset_index()

        )

        gender.columns = [

            "Gender",

            "Count"

        ]

        fig = px.bar(

            gender,

            x="Gender",

            y="Count",

            color="Gender",

            title="Customer Gender"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        fig = px.histogram(

            sales,

            x="Age",

            nbins=20,

            title="Customer Age Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    st.subheader("Recent Transactions")

    st.dataframe(

        sales.tail(10),

        use_container_width=True

    )
    # ==========================================================
# SALES ANALYTICS
# ==========================================================

elif page == "Sales Analytics":

    st.header("📊 Sales Analytics")

    st.markdown("---")

    category_filter = st.multiselect(

        "Select Product Category",

        sales["Product Category"].unique(),

        default=sales["Product Category"].unique()

    )

    filtered = sales[

        sales["Product Category"]

        .isin(category_filter)

    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Revenue",

            currency(

                filtered["Total Amount"].sum()

            )

        )

    with col2:

        st.metric(

            "Quantity",

            number(

                filtered["Quantity"].sum()

            )

        )

    with col3:

        st.metric(

            "Average Price",

            currency(

                filtered["Price per Unit"].mean()

            )

        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        revenue = (

            filtered

            .groupby("Product Category")

            ["Total Amount"]

            .sum()

            .reset_index()

        )

        fig = px.bar(

            revenue,

            x="Product Category",

            y="Total Amount",

            color="Product Category",

            title="Revenue by Category"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        quantity = (

            filtered

            .groupby("Product Category")

            ["Quantity"]

            .sum()

            .reset_index()

        )

        fig = px.bar(

            quantity,

            x="Product Category",

            y="Quantity",

            color="Product Category",

            title="Quantity Sold"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    sales_date = (

        filtered

        .groupby("Date")

        ["Total Amount"]

        .sum()

        .reset_index()

    )

    sales_date["Date"] = pd.to_datetime(

        sales_date["Date"]

    )

    fig = px.line(

        sales_date,

        x="Date",

        y="Total Amount",

        markers=True,

        title="Revenue Over Time"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Sales Dataset")

    st.dataframe(

        filtered,

        use_container_width=True

    )

    csv = filtered.to_csv(

        index=False

    )

    st.download_button(

        "⬇ Download Sales Data",

        csv,

        "sales_data.csv",

        "text/csv"

    )
# ==========================================================
# DEMAND FORECASTING
# ==========================================================

elif page == "Demand Forecasting":

    st.header("📈 Demand Forecasting")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Forecast Accuracy",

            f"{forecast_accuracy}%"

        )

    with col2:

        mae = abs(

            forecast["Actual"]

            -

            forecast["Predicted"]

        ).mean()

        st.metric(

            "Mean Absolute Error",

            f"{mae:.2f}"

        )

    with col3:

        rmse = (

            (

                (

                    forecast["Actual"]

                    -

                    forecast["Predicted"]

                ) ** 2

            ).mean()

        ) ** 0.5

        st.metric(

            "RMSE",

            f"{rmse:.2f}"

        )

    st.markdown("---")

    st.subheader("Actual vs Predicted Demand")

    fig = px.line(

        forecast,

        y=["Actual", "Predicted"],

        markers=True,

        title="Demand Forecast"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Prediction Error")

    forecast["Error"] = (

        forecast["Actual"]

        -

        forecast["Predicted"]

    )

    fig = px.bar(

        forecast,

        y="Error",

        title="Forecast Error"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Feature Importance")

    importance = pd.DataFrame({

        "Feature":[

            "Age",

            "Gender",

            "Product Category",

            "Price per Unit",

            "Year",

            "Month",

            "Day",

            "Quarter"

        ],

        "Importance":model.feature_importances_

    })

    importance = importance.sort_values(

        by="Importance",

        ascending=True

    )

    fig = px.bar(

        importance,

        x="Importance",

        y="Feature",

        orientation="h",

        title="Random Forest Feature Importance",

        color="Importance"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Forecast Result")

    st.dataframe(

        forecast,

        use_container_width=True

    )

    csv = forecast.to_csv(

        index=False

    )

    st.download_button(

        "⬇ Download Forecast",

        csv,

        "forecast_results.csv",

        "text/csv"

    )

# ==========================================================
# INVENTORY ANALYTICS
# ==========================================================

elif page == "Inventory Analytics":

    st.header("📦 Inventory Analytics")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Products",

            len(inventory)

        )

    with col2:

        st.metric(

            "Average EOQ",

            round(

                inventory["EOQ"].mean(),

                2

            )

        )

    with col3:

        st.metric(

            "Average Daily Demand",

            round(

                inventory["Average_Daily_Demand"].mean(),

                2

            )

        )

    st.markdown("---")

    st.subheader("Current Inventory")

    fig = px.bar(

        inventory,

        x="Product_Category",

        y="Current_Stock",

        color="Inventory_Status",

        title="Current Stock"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(

            inventory,

            x="Product_Category",

            y="EOQ",

            color="EOQ",

            title="Economic Order Quantity"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        fig = px.bar(

            inventory,

            x="Product_Category",

            y="Reorder_Point",

            color="Reorder_Point",

            title="Reorder Point"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    st.subheader("Safety Stock")

    fig = px.bar(

        inventory,

        x="Product_Category",

        y="Safety_Stock",

        color="Safety_Stock",

        title="Safety Stock"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Inventory Summary")

    st.dataframe(

        inventory,

        use_container_width=True

    )

    csv = inventory.to_csv(

        index=False

    )

    st.download_button(

        "⬇ Download Inventory Report",

        csv,

        "inventory_optimization.csv",

        "text/csv"

    )
# ==========================================================
# RISK ANALYSIS
# ==========================================================

elif page == "Risk Analysis":

    st.header("⚠️ Inventory Risk Analysis")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔴 High Risk",
            high_risk
        )

    with col2:
        st.metric(
            "🟠 Medium Risk",
            medium_risk
        )

    with col3:
        st.metric(
            "🟢 Low Risk",
            low_risk
        )

    st.markdown("---")

    st.subheader("Risk Level Distribution")

    risk_count = (
        risk["Risk_Level"]
        .value_counts()
        .reset_index()
    )

    risk_count.columns = [
        "Risk Level",
        "Count"
    ]

    fig = px.pie(
        risk_count,
        names="Risk Level",
        values="Count",
        hole=0.45,
        title="Inventory Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Risk Score by Product Category")

    fig = px.bar(

        risk,

        x="Product_Category",

        y="Risk_Score",

        color="Risk_Level",

        text="Risk_Score",

        title="Risk Score"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Recommendations")

    st.dataframe(

        risk[
            [
                "Product_Category",
                "Inventory_Status",
                "Risk_Level",
                "Risk_Score",
                "Recommendation"
            ]
        ],

        use_container_width=True

    )

    st.markdown("---")

    csv = risk.to_csv(index=False)

    st.download_button(

        "⬇ Download Risk Report",

        csv,

        "risk_analysis.csv",

        "text/csv"

    )

# ==========================================================
# PROJECT SUMMARY
# ==========================================================

st.markdown("---")

with st.expander("📄 Project Information", expanded=False):

    st.markdown("""

# Project FORESIGHT

### AI-Powered Inventory Analytics & Demand Forecasting

This project predicts customer demand using Machine Learning and provides inventory optimization and business insights for retail organizations.

### Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-Learn
- Plotly
- Joblib

### Modules

- Sales Analytics
- Demand Forecasting
- Inventory Optimization
- Risk Analysis

### Machine Learning Model

Random Forest Regressor

### Dataset

Retail Sales Dataset

""")

st.markdown("---")

st.subheader("📥 Download Reports")

col1, col2, col3 = st.columns(3)

with col1:

    st.download_button(

        "Sales CSV",

        sales.to_csv(index=False),

        "processed_retail_sales.csv",

        "text/csv"

    )

with col2:

    st.download_button(

        "Inventory CSV",

        inventory.to_csv(index=False),

        "inventory_optimization.csv",

        "text/csv"

    )

with col3:

    st.download_button(

        "Risk CSV",

        risk.to_csv(index=False),

        "risk_analysis.csv",

        "text/csv"

    )

st.markdown("---")

st.success("✅ Project Pipeline Executed Successfully")

st.info("""

Pipeline

Raw Dataset

↓

Preprocessing

↓

Demand Forecasting

↓

Inventory Optimization

↓

Risk Analysis

↓

Interactive Dashboard

""")

st.markdown("---")

st.caption(

    "© 2026 Project FORESIGHT | AI Powered Inventory Analytics & Demand Forecasting"

)