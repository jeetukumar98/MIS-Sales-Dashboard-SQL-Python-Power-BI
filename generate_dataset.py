"""
MIS Sales Project - synthetic dataset generator
Creates: customers.csv, products.csv, sales.csv, expenses.csv
Run: python generate_dataset.py
"""
import random
from datetime import date, timedelta

import pandas as pd

random.seed(42)

# ---------- Customers ----------
first = ["Rahul", "Amit", "Priya", "Sneha", "Vikas", "Neha", "Rohit", "Pooja", "Sanjay", "Anita",
         "Deepak", "Kavita", "Manoj", "Sunita", "Arun", "Meena", "Suresh", "Ritu", "Ajay", "Komal"]
last = ["Sharma", "Verma", "Singh", "Gupta", "Yadav", "Kumar", "Mishra", "Tiwari", "Chauhan", "Jain"]
cities = {
    "Delhi": "Delhi", "Noida": "Uttar Pradesh", "Ghaziabad": "Uttar Pradesh",
    "Gurgaon": "Haryana", "Faridabad": "Haryana", "Meerut": "Uttar Pradesh",
    "Lucknow": "Uttar Pradesh", "Jaipur": "Rajasthan",
}
segments = ["Retail", "Wholesale", "Corporate"]

customers = []
for cid in range(1, 201):
    city = random.choice(list(cities))
    customers.append({
        "customer_id": cid,
        "customer_name": f"{random.choice(first)} {random.choice(last)}",
        "city": city,
        "state": cities[city],
        "segment": random.choices(segments, weights=[60, 25, 15])[0],
        "join_date": date(2024, 1, 1) + timedelta(days=random.randint(0, 700)),
    })
customers_df = pd.DataFrame(customers)

# ---------- Products ----------
product_list = [
    ("Waterproofing Chemical 20L", "Chemicals", 2800, 2000),
    ("Waterproofing Chemical 5L", "Chemicals", 780, 560),
    ("Roof Coating Paint 10L", "Paint", 1900, 1350),
    ("Wall Putty 20kg", "Paint", 950, 700),
    ("Crack Filler Kit", "Repair", 450, 300),
    ("Bitumen Membrane Roll", "Membrane", 3500, 2600),
    ("PU Sealant Tube", "Repair", 320, 210),
    ("Tile Adhesive 20kg", "Construction", 620, 430),
    ("Basement Sealant 25L", "Chemicals", 4200, 3100),
    ("Cement Additive 5L", "Construction", 540, 380),
]
products_df = pd.DataFrame([
    {"product_id": i + 1, "product_name": n, "category": c, "unit_price": p, "cost_price": cp}
    for i, (n, c, p, cp) in enumerate(product_list)
])

# ---------- Sales ----------
start, end = date(2025, 1, 1), date(2026, 9, 30)
days = (end - start).days
payment_modes = ["UPI", "Cash", "Bank Transfer", "Cheque", "Credit"]
statuses = ["Paid", "Paid", "Paid", "Pending", "Partial"]
sales = []
for oid in range(1, 3001):
    d = start + timedelta(days=random.randint(0, days))
    # monsoon months (Jun-Sep) -> more waterproofing sales
    if d.month in (6, 7, 8, 9) and random.random() < 0.35:
        d = start + timedelta(days=random.randint(0, days))
    prod = products_df.sample(1, random_state=random.randint(0, 10**6)).iloc[0]
    qty = random.randint(1, 20)
    cust = customers_df.sample(1, random_state=random.randint(0, 10**6)).iloc[0]
    discount = random.choice([0, 0, 0, 5, 10])
    total = round(prod.unit_price * qty * (1 - discount / 100), 2)
    sales.append({
        "order_id": oid,
        "order_date": d,
        "customer_id": int(cust.customer_id),
        "product_id": int(prod.product_id),
        "quantity": qty,
        "discount_pct": discount,
        "total_amount": total,
        "payment_mode": random.choice(payment_modes),
        "payment_status": random.choice(statuses),
    })
sales_df = pd.DataFrame(sales).sort_values("order_date").reset_index(drop=True)

# ---------- Expenses ----------
exp_cats = {
    "Salary": (60000, 90000), "Rent": (18000, 22000), "Transport": (5000, 15000),
    "Electricity": (2500, 6000), "Marketing": (3000, 20000), "Misc": (1000, 8000),
}
expenses = []
eid = 1
cur = date(2025, 1, 1)
while cur <= end:
    for cat, (lo, hi) in exp_cats.items():
        expenses.append({
            "expense_id": eid,
            "expense_date": cur.replace(day=random.randint(1, 28)),
            "category": cat,
            "amount": random.randint(lo, hi),
        })
        eid += 1
    cur = date(cur.year + (cur.month == 12), (cur.month % 12) + 1, 1)
expenses_df = pd.DataFrame(expenses)

# ---------- Save ----------
customers_df.to_csv("customers.csv", index=False)
products_df.to_csv("products.csv", index=False)
sales_df.to_csv("sales.csv", index=False)
expenses_df.to_csv("expenses.csv", index=False)

print("customers:", len(customers_df))
print("products :", len(products_df))
print("sales    :", len(sales_df))
print("expenses :", len(expenses_df))
