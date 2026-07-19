# 📊 Project FORESIGHT
## AI-Powered Inventory Analytics & Demand Forecasting

Project FORESIGHT is a Machine Learning-based retail analytics system that helps businesses analyze sales performance, forecast product demand, optimize inventory, and assess inventory risk through an interactive Streamlit dashboard.

---

## 🚀 Features

- 📈 Sales Analytics Dashboard
- 🤖 Machine Learning Demand Forecasting
- 📦 Inventory Optimization
- ⚠️ Inventory Risk Analysis
- 📊 Interactive Visualizations
- 📥 Downloadable Reports
- 🎯 Business Insights

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Libraries
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Plotly
- Streamlit
- Joblib

### Machine Learning
- Random Forest Regressor

---

## 📂 Project Structure

```
Project-FORESIGHT/
│
├── app.py
│
├── data/
│   ├── raw/
│   │     retail_sales.csv
│   │
│   └── processed/
│         processed_retail_sales.csv
│         forecast_results.csv
│         inventory_optimization.csv
│         risk_analysis.csv
│
├── model/
│     forecasting_model.pkl
│
├── reports/
│   └── figures/
│
├── src/
│   ├── data/
│   │     data_loader.py
│   │     preprocess.py
│   │
│   ├── models/
│   │     demand_forecasting.py
│   │     inventory_optimizer.py
│   │     risk_scoring.py
│   │
│   └── visualization/
│         charts.py
│
├── requirements.txt
└── README.md
```

---

# 📊 Dashboard Modules

### 🏠 Dashboard
- Total Revenue
- Total Transactions
- Total Quantity Sold
- Forecast Accuracy
- Customer Insights
- Revenue Trend
- Revenue Distribution

---

### 📈 Sales Analytics
- Daily Sales Trend
- Revenue by Product Category
- Quantity Sold
- Customer Analysis
- Download Sales Report

---

### 🤖 Demand Forecasting

Machine Learning predicts future product demand using:

- Age
- Gender
- Product Category
- Price per Unit
- Date Features

Performance Metrics:

- MAE
- RMSE
- R² Score
- Feature Importance

---

### 📦 Inventory Analytics

Inventory metrics include:

- Average Daily Demand
- Current Stock
- Reorder Point
- Safety Stock
- Economic Order Quantity (EOQ)
- Inventory Status

---

### ⚠️ Risk Analysis

Risk analysis provides:

- Risk Score
- Risk Level
- Inventory Status
- Business Recommendation

---

# 📈 Machine Learning Workflow

```
Retail Dataset
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
Random Forest Regressor
      │
      ▼
Demand Forecast
      │
      ▼
Inventory Optimization
      │
      ▼
Risk Analysis
      │
      ▼
Interactive Dashboard
```

---

# 📁 Dataset

The project uses a Retail Sales Dataset containing:

- Transaction ID
- Date
- Customer ID
- Gender
- Age
- Product Category
- Quantity
- Price per Unit
- Total Amount

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/project-FORESIGHT.git
```

Move into the project

```bash
cd project-FORESIGHT
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Execute Pipeline

### Step 1

```bash
python src/data/preprocess.py
```

### Step 2

```bash
python src/models/demand_forecasting.py
```

### Step 3

```bash
python src/models/inventory_optimizer.py
```

### Step 4

```bash
python src/models/risk_scoring.py
```

### Step 5

```bash
python src/visualization/charts.py
```

---

# ▶️ Run Dashboard

```bash
streamlit run app.py
```

---

# 📊 Output Files

Generated automatically:

```
processed_retail_sales.csv

forecast_results.csv

inventory_optimization.csv

risk_analysis.csv

forecasting_model.pkl

Charts (.png)
```

---

# 📷 Dashboard Preview

Add screenshots here after running the project.

Example:

```
Dashboard.png

SalesAnalytics.png

DemandForecast.png

InventoryAnalytics.png

RiskAnalysis.png
```

---

# 🎯 Future Enhancements

- Deep Learning Forecasting (LSTM)
- Real-Time Sales Dashboard
- Supplier Management
- Stock Alert Notifications
- Cloud Deployment
- REST API Integration

---

# 👨‍💻 Developer

**Kameshwaran K**

B.Tech Artificial Intelligence & Data Science

JJ College of Engineering and Technology

India

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_PROFILE

---

# 📜 License

This project is developed for educational and internship purposes.

---

## ⭐ If you like this project, don't forget to star the repository!