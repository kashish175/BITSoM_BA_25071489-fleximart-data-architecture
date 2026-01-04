# --------Task 3.1: Star Schema Design Documentation ------

# Section 1: Schema Overview

## FACT TABLE: fact_sales 
 ### **Grain:** One row per product per order line item

### **Business Process :** Sales transactions

### **Measures (Numeric Facts) :**
- `quantity_sold` : Number of units sold
- `unit_price` : Price per unit at time of sale
- `discount_amount` : Discount applied
- `total_amount` : Final amount (quantity × unit_price - discount)

### **Foreign Keys:**
- `date_key` → dim_date
- `product_key` → dim_product
- `customer_key` → dim_customer

## DIMENSION TABLE: dim_date
### **Purpose :** Date dimension for time-based analysis 

### **Type :** Conformed dimension

### **Attributes :**
- `date_key (PK)` : Surrogate key (integer, format: YYYYMMDD)
- `full_date` : Actual date
- `day_of_week` : Monday, Tuesday, etc.
- `month` : 1-12
- `month_name` : January, February, etc.
- `quarter` : Q1, Q2, Q3, Q4
- `year` : 2023, 2024, etc.
- `is_weekend` : Boolean

## DIMENSION TABLE: dim_product
### **Purpose :** Stores descriptive attributes for all products to allow for filtering and grouping by category.

### **Type :** Conformed Dimension.
 
### **Attributes :**

- `product_key (PK)` : Surrogate key (integer).
- `product_id `: The original natural key from the NoSQL/Source system (e.g., "ELEC001").
- `product_name` : The full name of the product (e.g., "Samsung Galaxy S21 Ultra").
- `category` : High-level grouping (e.g., "Electronics").
- `subcategory` : More specific grouping (e.g., "Smartphones").
- `unit_price` :  Current retail price.

## DIMENSION TABLE: dim_customer
### **Purpose :** Stores customer demographic information for regional and personal sales analysis. 

### **Type :** Conformed Dimension.

 ### **Attributes :**
- `customer_key (PK)` : Surrogate key (integer).
- `customer_id` : The original unique identifier for the customer.
- `customer_name` : Full name of the customer.
- `email` : Contact information for communication analysis.
- `city` : The city where the customer resides (e.g., "Mumbai").
- `state` : Geographic state for regional reporting.
- `customer segment` : Consumer, Corporate, Small Business.

# Section 2: Design Decisions
## 1. Why you chose this granularity (transaction line-item level)
I chose the transaction line-item granularity for the fact table because it provides the most detailed level of data, allowing FlexiMart to analyze specific product performance within individual orders. This level of detail is essential for accurate discount and tax calculations per item and ensures that no critical business information is lost during the aggregation process.

## 2. Why surrogate keys instead of natural keys
I implemented surrogate keys (integers like product_key) instead of natural keys to decouple the data warehouse from operational source system changes. This strategy ensures data integrity,simplifies the ETL maintenance process, and significantly optimizes join performance during complex analytical queries by utilizing smaller integer-based indexes.

## 3. How this design supports drill-down and roll-up operations
This architecture inherently supports drill-down and roll-up operations. Users can perform a roll-up to view high-level quarterly sales trends using the dim_date hierarchy or a drill-down to examine specific daily sales at the city level via dim_customer. Similarly, products can be analyzed by broad categories or specific brands, providing FlexiMart with flexible, actionable business insights for better decision-making.


# Section 3: Sample Data Flow

## Source Transaction:
Order ID : 5001

Date : 2024-03-12

Customer : Amit Sharma (ID: C789)

Product : Laptop (ID: P102)

Quantity : 2

Unit Price : 1,200

Total : 2,400

## Becomes in Data Warehouse:
fact_sales: {
     sale_id: 1001,
      date_key: 20240312,
        product_key: 82,
         customer_key: 45,
          quantity_sold: 2,
           unit_price: 1200,
            total_amount: 2400 }


dim_date :	{
     date_key: 20240312,
      full_date: '2024-03-12',
       month: 3,
        year: 2024,
         quarter: 'Q1',
          month_name : March }

dim_customer :	{ 
    customer_key: 45, 
     customer_id: 'C789', 
      customer_name: 'Amit Sharma', 
       city: 'Delhi' ...}

dim_product :	{ 
    product_key: 82, 
     product_id: 'P102',
       product_name:'Laptop', 
        category: 'Electronics' }

**This flow demonstrates how transactional data is transformed into a structured star schema suitable for analytical reporting.**