# ✈️ AeroPulse — Airline Operations & Revenue Intelligence

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

> **End-to-End Airline Operations Analysis | EDA | Feature Engineering | MySQL Integration | Python Dashboard**

---

## 📌 Project Overview

AeroPulse is a real-world airline operations analytics project that analyses flight transaction data to uncover **delay patterns**, **revenue opportunities**, and **operational inefficiencies** across routes and aircraft types.

This project simulates a scenario where an airline operations team wants to move from gut-feel decisions to **evidence-based strategies** using data.

---

## 📊 Dataset

| Property | Details |
|----------|---------|
| File | `Airline_Operations_Revenue_Intelligence.csv` |
| Domain | Aviation / Airline Operations |
| Key Columns | `flight_date`, `origin`, `destination`, `aircraft_type`, `passenger_count`, `seat_capacity`, `delay_minutes`, `revenue` |

---

## 🎯 Business Problems Solved

| ID | Problem | Priority |
|----|---------|----------|
| P-01 | Which routes have the highest average delays? | 🔴 High |
| P-02 | Which aircraft types have low load factors? | 🔴 High |
| P-03 | Which routes generate the most revenue? | 🔴 High |
| P-04 | What is the on-time vs delay performance? | 🟡 Medium |
| P-05 | How many flights operate below 60% seat capacity? | 🟡 Medium |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Data cleaning, EDA, visualization |
| **Pandas** | Data manipulation & analysis |
| **Matplotlib** | Charts and 5-panel dashboard |
| **SQLAlchemy** | MySQL database connection |
| **MySQL** | Data storage & SQL queries |

---

## 📁 Project Structure

```
aeropulse-airline-operations/
│
├── project_4.py                                   ← Main analysis script
├── Airline_Operations_Revenue_Intelligence.csv    ← Raw dataset
├── README.md                                      ← Project documentation
├── .gitignore                                     ← Files to ignore
│
└── outputs/
    └── aeropulse_operations_dashboard.png         ← 5-panel dashboard (auto-generated)
```

---

## ⚙️ Feature Engineering

New columns created from raw data:

| Feature | Formula / Logic | Description |
|---------|----------------|-------------|
| `route` | origin + " → " + destination | Combined route name |
| `load_factor` | passenger_count / seat_capacity | How full the flight was |
| `delay_category` | ≤5 min = On-Time, ≤30 = Minor, >30 = Major | Delay classification |
| `day_type` | Mon–Fri = Weekday, Sat–Sun = Weekend | Day classification |

---

## 📈 Key Insights

- 🔴 **Top delay routes** identified — targeted for schedule & operational review
- ⚡ **Load factor below 60%** on several routes — significant revenue leakage opportunity
- 💰 **Top revenue routes** confirmed — priority for fleet and staffing investment
- 📅 **Weekend vs Weekday** patterns revealed in revenue distribution
- ✅ **On-time performance %** calculated across all routes

---

## 🖼️ Dashboard Preview

5-panel dashboard auto-generated on running the script:

| Panel | Chart |
|-------|-------|
| 1 | Top 10 Routes by Average Delay (Bar) |
| 2 | Load Factor by Aircraft Type (Bar + 60% threshold line) |
| 3 | Top 10 Revenue Routes (Bar) |
| 4 | Delay Category Distribution (Bar with counts) |
| 5 | Delay vs Load Factor (Scatter plot) |
| 6 | Weekday vs Weekend Revenue (Pie) |

---

## 🚀 How to Run

### Step 1 — Install required libraries
```bash
pip install pandas matplotlib sqlalchemy mysql-connector-python
```

### Step 2 — Place your CSV file
Make sure `Airline_Operations_Revenue_Intelligence.csv` is in the **same folder** as `project_4.py`.

### Step 3 — Update MySQL credentials *(optional)*
In `project_4.py`, update line in `database_integration()`:
```python
engine = create_engine(
    "mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/YOUR_DATABASE"
)
```
> 💡 If you don't have MySQL, simply comment out the `database_integration(df)` line in `main()`.

### Step 4 — Run the script
```bash
python project_4.py
```

---

## 📂 Output Files Generated

| File | Description |
|------|-------------|
| `aeropulse_operations_dashboard.png` | 5-panel visual dashboard |

---

## 👩‍💻 Author

**Srinagadivya Chunchula** — Data Analyst

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/sri-naga-divya-chunchula-955b56288)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?logo=github)](https://github.com/SrinagadivyaChunchula)
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:srinagadivyac@gmail.com)

---

## 📜 Related Projects

| Project | Link |
|---------|------|
| 🏦 Retail Lending Risk Intelligence | [GitHub](https://github.com/SrinagadivyaChunchula/retail-lending-risk-intelligence) |
| 🛒 GMart Retail Sales Analytics | [GitHub](https://github.com/SrinagadivyaChunchula/gmart-retail-sales-analytics) |
| 👥 Customer Intelligence & Revenue Optimization | [GitHub](https://github.com/SrinagadivyaChunchula/customer-intelligence-revenue-optimization) |

---

*Part of Data Analytics Portfolio | Srinagadivya Chunchula | 2026*
