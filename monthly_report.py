"""
Automated MIS Monthly Report
MySQL (vw_sales_report + expenses) se data nikal ke Excel report banata hai.

Install : pip install pandas sqlalchemy pymysql openpyxl
Run     : python monthly_report.py            (latest month ka report)
          python monthly_report.py 2026 8     (kisi specific month ka report)
"""
import sys
from datetime import date

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ---- apni MySQL details yahan daalo ----
USER = "root"
PASSWORD = "Raj@12345"   # @ jaisa character ho to bhi chalega
HOST = "localhost"
DB = "mis_sales"

engine = create_engine(
    URL.create("mysql+pymysql", username=USER, password=PASSWORD, host=HOST, database=DB)
)

# ---------- Data load ----------
sales = pd.read_sql("SELECT * FROM vw_sales_report", engine, parse_dates=["order_date"])
expenses = pd.read_sql("SELECT * FROM expenses", engine, parse_dates=["expense_date"])

# ---------- Month select ----------
if len(sys.argv) == 3:
    year, month = int(sys.argv[1]), int(sys.argv[2])
else:
    latest = sales["order_date"].max()
    year, month = latest.year, latest.month

m_sales = sales[(sales.order_date.dt.year == year) & (sales.order_date.dt.month == month)]
m_exp = expenses[(expenses.expense_date.dt.year == year) & (expenses.expense_date.dt.month == month)]

if m_sales.empty:
    sys.exit(f"{year}-{month:02d} ka koi sales data nahi mila.")

# ---------- KPIs ----------
revenue = m_sales["total_amount"].sum()
profit = m_sales["profit"].sum()
total_exp = m_exp["amount"].sum()
pending = m_sales.loc[m_sales.payment_status != "Paid", "total_amount"].sum()

summary = pd.DataFrame({
    "KPI": ["Total Orders", "Revenue", "Gross Profit", "Total Expenses",
            "Net Profit (Gross - Expenses)", "Pending/Partial Payments"],
    "Value": pd.Series([len(m_sales), round(revenue, 2), round(profit, 2), round(total_exp, 2),
                        round(profit - total_exp, 2), round(pending, 2)], dtype=object),
})

# ---------- Breakdown tables ----------
by_product = (m_sales.groupby("product_name")
              .agg(orders=("order_id", "count"), qty=("quantity", "sum"),
                   revenue=("total_amount", "sum"), profit=("profit", "sum"))
              .sort_values("revenue", ascending=False).round(2).reset_index())

by_city = (m_sales.groupby("city")
           .agg(orders=("order_id", "count"), revenue=("total_amount", "sum"))
           .sort_values("revenue", ascending=False).round(2).reset_index())

pending_df = (m_sales[m_sales.payment_status != "Paid"]
              [["order_id", "order_date", "customer_name", "city", "total_amount", "payment_status"]]
              .sort_values("total_amount", ascending=False))
pending_df["order_date"] = pending_df["order_date"].dt.date

exp_df = m_exp.groupby("category")["amount"].sum().sort_values(ascending=False).reset_index()

# ---------- Excel export ----------
out = f"MIS_Report_{year}_{month:02d}.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False)
    by_product.to_excel(writer, sheet_name="By Product", index=False)
    by_city.to_excel(writer, sheet_name="By City", index=False)
    pending_df.to_excel(writer, sheet_name="Pending Payments", index=False)
    exp_df.to_excel(writer, sheet_name="Expenses", index=False)

    # column width thoda theek karo
    for ws in writer.book.worksheets:
        for col in ws.columns:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col) + 3
            ws.column_dimensions[col[0].column_letter].width = min(width, 40)

print(f"Report ready: {out}")
print(summary.to_string(index=False))