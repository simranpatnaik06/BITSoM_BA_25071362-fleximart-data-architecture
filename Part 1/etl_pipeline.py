# =========================
# STEP 1: LOAD CSV FILES SAFELY
# =========================

import pandas as pd
import os

print("Current directory:", os.getcwd())

# Load CSV files
customers = pd.read_csv("data/customers_raw.csv")
products  = pd.read_csv("data/products_raw.csv")
sales     = pd.read_csv("data/sales_raw.csv")

# Standardize column names
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

customers = clean_columns(customers)
products  = clean_columns(products)
sales     = clean_columns(sales)

print("Customers columns:", customers.columns.tolist())
print("Products columns:", products.columns.tolist())
print("Sales columns:", sales.columns.tolist())


# =========================
# STEP 2: DROP UNWANTED COLUMNS (SAFE)
# =========================

def drop_if_exists(df, cols):
    for col in cols:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    return df

customers = drop_if_exists(customers, ["id"])
products  = drop_if_exists(products, ["id"])
sales     = drop_if_exists(sales, ["id", "transaction_id"])

# Rename transaction_date → order_date only if exists
if "transaction_date" in sales.columns:
    sales.rename(columns={"transaction_date": "order_date"}, inplace=True)

print("After cleanup:")
print("Customers columns:", customers.columns.tolist())
print("Products columns:", products.columns.tolist())
print("Sales columns:", sales.columns.tolist())


# =========================
# STEP 3: CREATE SUBTOTAL (SAFE)
# =========================

required_cols = {"quantity", "unit_price"}
if required_cols.issubset(sales.columns):
    sales["subtotal"] = sales["quantity"] * sales["unit_price"]
else:
    raise ValueError("quantity or unit_price column missing in sales data")

print("Subtotal created successfully")
print(sales.head())


# =========================
# STEP 4: CONVERT DATE COLUMNS (SAFE)
# =========================

if "registration_date" in customers.columns:
    customers["registration_date"] = pd.to_datetime(
        customers["registration_date"], errors="coerce"
    )

if "order_date" in sales.columns:
    sales["order_date"] = pd.to_datetime(
        sales["order_date"], errors="coerce"
    )

print("Dates converted successfully")


# =========================
# STEP 5: FINAL CLEANUP BEFORE DB LOAD
# =========================

# Rename order_date → sale_date only if exists
if "order_date" in sales.columns:
    sales.rename(columns={"order_date": "sale_date"}, inplace=True)

# Convert IDs safely
def safe_int_convert(df, col):
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

safe_int_convert(customers, "customer_id")
safe_int_convert(products, "product_id")
safe_int_convert(sales, "customer_id")
safe_int_convert(sales, "product_id")

print("Data ready for database load")

print("Customers sample:")
print(customers.head())

print("Products sample:")
print(products.head())

print("Sales sample:")
print(sales.head())

# =========================
# STEP 6: CONNECT TO MYSQL DATABASE
# =========================

from sqlalchemy import create_engine

# Replace these with your actual MySQL credentials
db_username = "root"            # your MySQL username
db_password = "simran666"       # your new MySQL password
db_host     = "localhost"
db_port     = "3306"
db_name     = "fleximart"

# Create connection string
connection_string = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create SQLAlchemy engine
engine = create_engine(connection_string)
print("Database engine created successfully")

from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY,
        customer_name VARCHAR(100)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100),
        category VARCHAR(50),
        price FLOAT,
        stock_quantity INT
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        order_date DATE,
        status VARCHAR(20)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        unit_price FLOAT,
        subtotal FLOAT
    );
    """))

print("Tables created successfully")

# =========================
# STEP 7A: TRUNCATE TABLES
# =========================
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE order_items"))
    conn.execute(text("TRUNCATE TABLE orders"))
    conn.execute(text("TRUNCATE TABLE sales"))
    conn.execute(text("TRUNCATE TABLE customers"))
    conn.execute(text("TRUNCATE TABLE products"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

print("Tables truncated")

customers = customers.drop_duplicates(subset=["customer_id"])
products  = products.drop_duplicates(subset=["product_id"])
sales     = sales.drop_duplicates()

customers_to_load = customers[[
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "city",
    "registration_date"
]]

customers_to_load.to_sql(
    name="customers",
    con=engine,
    if_exists="append",
    index=False
)

print("Customers loaded")

products_to_load = products[[
    "product_id",
    "product_name",
    "category",
    "price",
    "stock_quantity"
]]

products_to_load.to_sql(
    name="products",
    con=engine,
    if_exists="append",
    index=False
)

print("Products loaded")

# Step: Keep only valid customer_id and product_id in sales
valid_customers = pd.read_sql("SELECT customer_id FROM customers", engine)
valid_products  = pd.read_sql("SELECT product_id FROM products", engine)

# Merge to clean sales
sales_clean = sales.merge(valid_customers, on="customer_id")
sales_clean = sales_clean.merge(valid_products, on="product_id")

# =========================
# STEP: Generate order_id
# =========================
sales_clean = sales_clean.copy()
sales_clean["order_id"] = range(1, len(sales_clean) + 1)

# Rename sale_date to order_date to match MySQL table
sales_clean.rename(columns={"sale_date": "order_date"}, inplace=True)

# Prepare orders DataFrame
orders_to_load = sales_clean[[
    "order_id",
    "customer_id",
    "order_date",
    "status"
]].drop_duplicates(subset=["order_id"])

# Load orders into MySQL
orders_to_load.to_sql(
    name="orders",
    con=engine,
    if_exists="append",
    index=False
)

print("Orders loaded")

# =========================
# STEP: Prepare order_items
# =========================

# Generate order_item_id automatically in DB (AUTO_INCREMENT), so we don't need it here
order_items_to_load = sales_clean[[
    "order_id",
    "product_id",
    "quantity",
    "unit_price",
    "subtotal"
]]

# Load order_items into MySQL
order_items_to_load.to_sql(
    name="order_items",
    con=engine,
    if_exists="append",
    index=False
)

print("Order items loaded")

