# FlexiMart NoSQL Analysis

## Section A: Limitations of RDBMS (150 words)

Relational databases like MySQL are rigid and rely on predefined schemas. FlexiMart’s diverse product catalog poses challenges because different product types have unique attributes; for example, laptops require RAM and processor specifications, while shoes require size and color. Adding new product types often requires altering table structures, which is time-consuming and error-prone. Storing customer reviews, which are nested and variable in length, is difficult in relational tables without creating multiple join tables, leading to complex queries and degraded performance. Frequent schema changes for new product types would cause downtime and migration overhead. Overall, traditional RDBMS structures make it cumbersome to accommodate flexible, hierarchical, and evolving product data efficiently.

---

## Section B: NoSQL Benefits (150 words)

MongoDB, a document-oriented NoSQL database, addresses these limitations effectively. It uses a *flexible schema, allowing each product document to store different fields based on product type without altering a global structure. **Embedded documents* enable storing customer reviews directly within product documents, simplifying queries and improving read performance. For example, the reviews array can hold multiple review objects for each product. MongoDB also supports *horizontal scalability*, distributing data across multiple nodes to handle large product catalogs and high read/write loads. Aggregation pipelines allow efficient analysis of nested data, such as calculating average ratings per product. This flexibility reduces the need for complex joins and schema migrations, enabling rapid addition of new product categories, dynamic attributes, and nested customer interactions, which is not practical in traditional relational systems.

---

## Section C: Trade-offs (100 words)

While MongoDB offers flexibility, there are trade-offs. First, it *lacks strict ACID transactions* across multiple documents compared to MySQL, which can be critical for financial or order-related operations. Second, data redundancy is more likely because embedded documents may duplicate information, increasing storage usage and making updates harder. Additionally, complex relational queries involving multiple entities can be less efficient in MongoDB, requiring careful schema design. Indexing and query optimization require more planning than in RDBMS. Overall, while MongoDB is ideal for flexible, hierarchical product data, critical transactional or heavily relational workloads may still benefit from MySQL.
