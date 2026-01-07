# FlexiMart Database Schema Documentation

## 1. Entity-Relationship Description

### ENTITY: customers
*Purpose:* Stores customer information.  
*Attributes:*
- customer_id: Unique identifier (Primary Key)
- first_name: Customer's first name
- last_name: Customer's last name
- email: Customer's email address
- phone: Customer's contact number
- city: Customer's city
- registration_date: Date of customer registration

*Relationships:*  
- One customer can place *many orders* → 1:M relationship with orders table

### ENTITY: products
*Purpose:* Stores product information available in FlexiMart.  
*Attributes:*
- product_id: Unique identifier (Primary Key)
- product_name: Name of the product
- category: Product category (e.g., Electronics, Clothing)
- price: Price of the product
- stock_quantity: Quantity available in stock

*Relationships:*  
- One product can appear in *many order_items* → 1:M relationship with order_items table

### ENTITY: orders
*Purpose:* Stores customer orders.  
*Attributes:*
- order_id: Unique identifier for each order (Primary Key)
- customer_id: References the customer who placed the order (Foreign Key)
- order_date: Date when the order was placed
- status: Current status of the order (e.g., Pending, Completed, Cancelled)

*Relationships:*  
- One order belongs to *one customer* → M:1 relationship with customers table  
- One order can contain *many order_items* → 1:M relationship with order_items table

### ENTITY: order_items
*Purpose:* Stores details of products included in each order.  
*Attributes:*
- order_item_id: Unique identifier for each order item (Primary Key)
- order_id: References the order this item belongs to (Foreign Key)
- product_id: References the product being ordered (Foreign Key)
- quantity: Number of units of the product in the order
- unit_price: Price per unit at the time of order
- subtotal: Total price for this item (quantity * unit_price)

*Relationships:*  
- One order item belongs to *one order* → M:1 relationship with orders table  
- One order item refers to *one product* → M:1 relationship with products table

Normalization Explanation

Purpose: Ensure the database design avoids redundancy and anomalies.

Functional Dependencies:

customers: customer_id → first_name, last_name, email, phone, city, registration_date

products: product_id → product_name, category, price, stock_quantity

orders: order_id → customer_id, order_date, status

order_items: order_item_id → order_id, product_id, quantity, unit_price, subtotal

3NF Justification:

All tables have a primary key that uniquely identifies each record.

No table contains non-prime attributes that depend on other non-prime attributes.

All non-key attributes are fully functionally dependent on the primary key.

Each table stores information about a single entity: customers (customer info), products (product info), orders (order info), order_items (products in each order).

Avoiding Anomalies:

Update Anomaly: Changing customer info only requires updating the customers table. No duplicates exist across other tables.

Insert Anomaly: Can add a new product or customer without requiring an order.

Delete Anomaly: Deleting an order does not remove customer or product info.

Sample Data Representation

Customers Sample Data:

Customer 1: Rahul Sharma, rahul.sharma@gmail.com
, 9876543210, Bangalore, 2023-01-15

Customer 2: Priya Patel, priya.patel@yahoo.com
, 9988776564, Mumbai, 2023-02-20

Customer 3: Amit Kumar, amit.kumar@gmail.com
, 9765432109, Delhi, 2023-03-10

Products Sample Data:

Product 1: Laptop, Electronics, 75000, 50

Product 2: Smartphone, Electronics, 35000, 100

Product 3: Desk Chair, Furniture, 5000, 25

Orders Sample Data:

Order 1: Customer 1, 2024-01-15, Completed

Order 2: Customer 2, 2024-01-16, Completed

Order 3: Customer 3, 2024-01-15, Completed

Order Items Sample Data:

Order Item 1: Order 1, Product 1, 1, 75000, 75000

Order Item 2: Order 2, Product 2, 2, 35000, 70000

Order Item 3: Order 3, Product 3, 1, 5000, 5000
