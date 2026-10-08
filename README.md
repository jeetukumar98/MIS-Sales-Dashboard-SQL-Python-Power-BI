<img width="604" height="338" alt="image" src="https://github.com/user-attachments/assets/10c9bf45-b97a-424d-8505-e794a1dab240" /># MIS Sales Dashboard: SQL + Python + Power BI

An end-to-end MIS (Management Information System) reporting project. Sales and expense data is stored in **MySQL**, processed and automated with **Python**, and visualised in a **Power BI** dashboard.

> **Note:** The dataset is synthetic (generated with Python) and is used for learning and portfolio purposes only.

## Dashboard

"D:\Mis Sales Project\Dashboard image.png"

*(Replace this image with a screenshot of your own Power BI dashboard.)*

## Tech Stack

| Tool | Used for |
|------|----------|
| MySQL | Database design, JOINs, views |
| Python (pandas, SQLAlchemy) | Data generation, loading, automated Excel reports |
| Power BI | DAX measures, dashboard, map visual |

## Dataset

| Table | Rows | Description |
|-------|------|-------------|
| `customers` | 200 | Customer name, city, state, segment |
| `products` | 10 | Product, category, unit price, cost price |
| `sales` | 3,000 | Orders from Jan 2025 to Sep 2026 with payment status |
| `expenses` | 126 | Monthly expenses by category |

## Project Structure

```
mis_project/
├── generate_dataset.py     # creates the 4 CSV files
├── schema.sql              # MySQL tables + vw_sales_report view
├── load_to_mysql.py        # loads CSVs into MySQL
├── monthly_report.py       # generates monthly Excel report
├── customers.csv
├── products.csv
├── sales.csv
├── expenses.csv
└── dashboard_preview.png
```

## How to Run

1. Install packages: `pip install pandas sqlalchemy pymysql openpyxl`
2. Generate data: `python generate_dataset.py`
3. Run `schema.sql` in MySQL Workbench (creates database `mis_sales`)
4. Add your MySQL password in `load_to_mysql.py`, then run `python load_to_mysql.py`
5. Generate the monthly report: `python monthly_report.py` (or `python monthly_report.py 2026 8` for a specific month)
6. Open Power BI Desktop, connect to MySQL database `mis_sales`, load `vw_sales_report` and `expenses`

## Key Metrics (DAX)

```
Revenue = SUM(vw_sales_report[total_amount])
Profit = SUM(vw_sales_report[profit])
Total Expenses = SUM(expenses[amount])
Net Profit = [Profit] - [Total Expenses]
Pending Amount = CALCULATE([Revenue], vw_sales_report[payment_status] <> "Paid")
Profit Margin % = DIVIDE([Profit], [Revenue])
```

Gross profit is calculated in SQL as `total_amount - cost_price * quantity`. Net profit is gross profit minus expenses.

## Dashboard Contents

- KPI cards: Revenue, Gross Profit, Net Profit, Pending Payments, Orders
- Monthly revenue and profit trend
- City-wise revenue (bar chart and map)
- Category-wise revenue (clustered bar chart)
- Product performance table with data bars
- Slicers: year, segment, payment status

## Automation

`monthly_report.py` reads data from MySQL and creates an Excel report with 5 sheets: Summary, By Product, By City, Pending Payments and Expenses.

## Author

**Jeetu Kumar**
MIS Executive moving into Data Analytics
