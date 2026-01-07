# FlexiMart Star Schema Design

## Section 1: Schema Overview

### Fact Table: fact_sales
- *Grain:* One row per product per order line item  
- *Business Process:* Sales transactions  
- *Measures (Numeric Facts):*
  - quantity_sold: Number of units sold
  - unit_price: Price per unit at time of sale
  - discount_amount: Discount applied
  - total_amount: Final amount (quantity_sold × unit_price - discount_amount)
- *Foreign Keys:*
  - date_key → dim_date
  - product_key → dim_product
  - customer_key → dim_customer

### Dimension Table: dim_date
- *Purpose:* Date dimension for time-based analysis  
- *Type:* Conformed dimension  
- *Attributes:*
  - date_key (PK): Surrogate key (integer, format: YYYYMMDD)
  - full_date: Actual date
  - day_of_week: Monday, Tuesday, etc.
  - month: 1-12
  - month_name: January, February, etc.
  - quarter: Q1, Q2, Q3, Q4
  - year: 2023, 2024, etc.
  - is_weekend: Boolean

### Dimension Table: dim_product
- *Purpose:* Product attributes for sales analysis  
- *Attributes:*
  - product_key (PK): Surrogate key
  - product_name
  - category
  - subcategory
  - brand
  - price

### Dimension Table: dim_customer
- *Purpose:* Customer details for segmentation and reporting  
- *Attributes:*
  - customer_key (PK): Surrogate key
  - customer_name
  - city
  - email
  - phone
  - registration_date

---

## Section 2: Design Decisions

The granularity of the fact_sales table is at the transaction line-item level, meaning each row represents one product in one order. This allows detailed analysis of individual products per order, supporting precise aggregation and reporting. Surrogate keys are used for the dimensions instead of natural keys to ensure consistency and avoid dependency on changing business IDs, simplifying joins and improving performance.  

This star schema design supports drill-down and roll-up operations efficiently; for example, sales can be rolled up by month, quarter, or year using dim_date, or by product category using dim_product. Customers can be analyzed by city or registration year. This structure allows fast queries and aggregation, essential for analytical dashboards and business intelligence reports.

---

## Section 3: Sample Data Flow

*Source Transaction:*  
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

*Data Warehouse Representation:*

*fact_sales:*  
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}

