
# ----------Task 1.2: Database Schema Documentation-------

# 1. Entity-Relationship Description 

# ENTITY : customers
### Purpose :
 Stores customer information

### Attributes:
  - `customer_id :` Unique identifier (Primary Key)
  - `first_name :` Customer's first name
  - `last_name :` Customer's last name
  - `email :` Customer's email address
  - `phone :` Customer's contact number
  - `city :` Geographic location for shipping/demographics
  - `registration_date :` The date the customer account was originally created.

### Relationships :
  - One customer can place **MANY orders** (1:M relationship with `orders`)
  

# ENTITY : products
### Purpose : 
 Maintains the inventory catalog.

### Attributes : 
- `product_id :` Unique identifier (Primary Key) 
- `product_name :`  Product's name
- `category :` Product's category
-  `price :` Product's price
-  `stock_quantity :` Available stock of the product

### Relationships:
- One product can appear in **MANY order items** (1:M relationship with `order_items`).


# ENTITY: orders
### Purpose : 
 Stores transaction header information and order fulfillment status.

### Attributes :
- `order_id :` Unique identifier (Primary Key)
- `customer_id :` Link to the customer who placed the order(Foreign Key)
- `order_date:` Date the purchase was made
- `total_amount :` The final total cost for all items in the order.
- `status :` The current fulfillment stage of the order (e.g., Completed, pending).

### Relationships :
- Many orders belong to **ONE customer** (M:1).
- One order contains **MANY order items** (1:M relationship with `order_items`).


# ENTITY: order_items
### Purpose :
  Stores line-level details for each product within a order.

### Attributes :
- `order_item_id :` Unique identifier (Primary Key).
- `order_id :` Reference to the parent order (Foreign Key).
- `product_id :` Reference to the product being purchased (Foreign Key).
- `quantity :` The number of units of the product purchased.
- `unit_price :` The price of a single unit of the product at the time of purchase.
- `subtotal :` The calculated cost for this line item.

### Relationships :
- Many order items can have **ONE order** (M:1 relationship with `orders`).
- **One product** can be part of Many order_items (1:M relationship with `products`).
- Order_items resolves the **Many-to-Many** relationship between `orders` and `products`.


#  2. Normalization Explanation

The FlexiMart database schema is designed following the principles of the Third Normal Form (3NF) to ensure data integrity, minimize redundancy, and optimize storage efficiency.

 ## First Normal Form (1NF):
   The design achieves 1NF because every table has a defined Primary Key (such as customer_id or product_id), and all attributes contain atomic, single values. There are no repeating groups or multi-valued attributes, ensuring that each cell in the database contains only one piece of information.

 ## Second Normal Form (2NF): 
   The schema satisfies 2NF because it meets all 1NF requirements and ensures that all non-key attributes are fully functionally dependent on the entire Primary Key. In the order_items table,For example, in the products table, the price is determined solely by the product_id.

 ## Third Normal Form (3NF): 
   The design reaches 3NF by removing transitive dependencies. Non-key attributes do not depend on other non-key attributes. For example, customer contact information is stored in the customers table; the orders table only stores the customer_id. This structure prevents several critical issues:

- ### Insert Anomalies:
  We can add a new product to the products table without needing an existing order.

- ### Update Anomalies:
  If a product’s price changes, we update it in one row in the products table rather than searching through thousands of sales records.

- ### Delete Anomalies:
  Deleting a cancelled order from the orders table does not accidentally delete the customer’s profile or the product’s information from the system.



# 3. Sample Data Representation 

## **Table: customers**
| customer_id | first_name | last_name | email |phone | city | registration_date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Rahul | Sharma | rahul.sharma@gmail.com  | +91-9876543210	| Bangalore |  2023-01-15 |
| 2 | Priya | Patel  | priya.patel@yahoo.com   | +91-9988776655 | Mumbai    |  2023-02-20 |
| 3 | Amit  | Kumar  | no_email_0@fleximart.com| +91-9765432109	| Delhi     |  2023-03-10 |


## **Table: products**
| product_id | product_name | category | price | stock_quantity |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Samsung Galaxy S21 |	Electronics |   45999.00 |	150 |
| 2	| Nike Running Shoes |	Fashion     |  3499.00   |  80  |
| 3	|  Apple MacBook Pro |  Electronics	|    0.00	 |  45  |


## **Table: orders**
| order_id | customer_id | order_date | total_amount | status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1 |	2024-01-15 | 45999.00 |	Completed |
| 2	| 2 |	2024-01-16 | 5998.00  |	Completed |
| 3 | 3	|   2024-01-15 | 52999.00 |	Completed |


## **Table: order_items**
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 2 | 4 | 2 | 2999.00  | 5998.00   |
| 3 | 3 | 7 | 1 | 52999.00 | 52999.00 |


