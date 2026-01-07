# FlexiMart Data Architecture Project

**Student Name:** Simran Patnaik  
**Student ID:** BITSoM_BA_25071362  
**Email:** simranpatnaik07@gmail.com  
**Date:** 07/01/2026


## Project Overview

This project implements a complete data architecture solution for FlexiMart using MySQL and Python. It covers transactional database design, ETL processing, NoSQL analysis, and data warehouse–style analytics. All three parts of the project are implemented and executed within a single MySQL database named `fleximart`.

---

## Repository Structure
 
BITSoM_BA_25071362-fleximart-data-architecture/
│
├── README.md
├── .gitignore
│
├── data/
│   ├── customers_raw.csv
│   ├── products_raw.csv
│   └── sales_raw.csv
│
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   ├── data_quality_report.txt
│   └── requirements.txt
│
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
│
└── part3-datawarehouse/
    ├── star_schema_design.md
    ├── warehouse_schema.sql
    ├── warehouse_data.sql
    └── analytics_queries.sql

---

## Raw Data Files

The `data/` folder contains the original raw CSV files used as input for the ETL pipeline in Part 1.

- `customers_raw.csv` – customer demographic and registration data  
- `products_raw.csv` – product details and categories  
- `sales_raw.csv` – transactional sales records  

These files are extracted, transformed, and loaded into MySQL tables using the ETL pipeline.

---

## Technologies Used

- Python 3.x  
- pandas  
- mysql-connector-python  
- MySQL 8.0  
- MongoDB (for NoSQL analysis)

---

## Database Implementation Note

All three parts of this project (ETL, NoSQL-related analysis, and Data Warehouse analytics) are implemented using a **single MySQL database named `fleximart`**.

The data warehouse schema (fact and dimension tables) is created within the same database for simplicity and consistency, instead of using a separate `fleximart_dw` database.

---

## Setup Instructions

### MySQL Database Setup

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE fleximart;"

# Run Part 1 – ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 – Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 – Data Warehouse Schema
mysql -u root -p fleximart < part3-datawarehouse/warehouse_schema.sql

# Run Part 3 – Data Warehouse Data
mysql -u root -p fleximart < part3-datawarehouse/warehouse_data.sql

# Run Part 3 – OLAP Analytics Queries
mysql -u root -p fleximart < part3-datawarehouse/analytics_queries.sql

