# ------- Task 2.1: NoSQL Justification Report ---------

# NoSQL Justification Report: FlexiMart Database Analysis 

# Section A: Limitations of RDBMS
The current relational database (MySQL) faces significant operational hurdles as FlexiMart expands its inventory to include highly diverse product types.

- ## Rigid Schema Constraints:
   In a table-based system, adding products with unique attributes—such as RAM for laptops or material for shoes—forces the database to include numerous "nullable" columns. This results in sparse, inefficient tables where most cells are empty.

- ## Costly Schema Migrations: 
  Frequent inventory updates necessitate constant schema changes. Performing ALTER TABLE operations on a live production database with millions of rows can cause significant downtime and performance lag.

- ## Relational Joins for Nested Data:
  RDBMS struggles with nested data, such as customer reviews. Storing reviews in a relational model requires separate tables and resource-intensive JOIN operations. As volume grows, these joins become a major bottleneck, preventing a responsive user experience.


# Section B: NoSQL Benefits
Transitioning to a NoSQL database like MongoDB provides FlexiMart with the agility and scale needed for rapid global growth.

- ## Flexible Document Schema:
  MongoDB utilizes a dynamic schema based on JSON-like structures. This allows each product entry to store only relevant attributes; for example, a laptop document can contain "Processor" fields without being forced to accommodate "Shoe Size" fields.

- ## Efficient Data Embedding:  
  FlexiMart can store customer reviews directly within the product document using arrays. This eliminates the need for complex JOINs, allowing the application to retrieve all product details in a single, lightning-fast read operation.

- ## Horizontal Scalability (Sharding): 
  Unlike MySQL’s vertical scaling, MongoDB uses sharding to distribute data across multiple servers. This allows FlexiMart to handle massive traffic spikes during holiday sales by simply adding more commodity hardware to the cluster.
 

# Section C: Trade-offs (approx. 100 words)
Despite the flexibility, moving to MongoDB involves specific trade-offs regarding data management.

- ## Data Redundancy: 
  NoSQL often relies on embedding data to improve speed, which leads to duplication. For instance, customer names might be repeated in multiple order documents, increasing storage costs and making global updates more complex.

- ## ACID Compliance Challenges: 
  MongoDB sacrifices the Strict ACID compliance found in RDBMS to achieve horizontal scalability.MongoDB does not support multi-document JOINs and complex ACID transactions as robustly as MySQL. This makes it less suitable for critical financial auditing or inventory accounting where absolute mathematical consistency is mandatory.