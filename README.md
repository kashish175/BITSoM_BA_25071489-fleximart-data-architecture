# FlexiMart Data Architecture Project

**Student Name:** Kashish Agrawal
**Student ID:** BITSoM_BA_25071489
**Email:** akapil873@gmail.com
**Date:** 03/01/2026

## Project Overview 

I have built an integrated data architecture for FlexiMart that includes an ETL pipeline for relational data, a NoSQL catalog for flexible product management, and a specialized Data Warehouse using a Star Schema. This system enables complex OLAP analytics, such as monthly sales trends and customer segmentation based on purchasing behavior.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

1. I discovered that a Star Schema is much more efficient for reporting than a standard relational database because it reduces the number of complex joins needed to get a full picture of sales performance.

2. Working on the OLAP queries showed me how powerful Window Functions like OVER() are for calculating market share and contribution percentages without having to write multiple nested subqueries.

3. I realized the importance of using surrogate keys (like date_key as an integer) to keep the data warehouse performant and easy to index.

4. I learned that data realism—like adding weekend spikes and customer segments—makes the final analytical reports much more useful for business decision-making.

## Challenges Faced

1. # Data Cleaning :
 I initially filled missing product prices with a default value of 0.00, but I realized this would skew the revenue analytics so, I researched more robust data cleaning techniques and updated the ETL pipeline to use Median Imputation. By grouping products by category and applying the median price, I ensured that the data remained realistic.

2. # Customer Segmentation Logic: 
  Creating the 'High', 'Medium', and 'Low' value segments was tricky. I decided to use a Common Table Expression(CTE) to pre-calculate total spending per customer first, which made the final CASE statement much cleaner and easier to read.

3. # Foreign Key Dependencies:
 I initially tried to load all the data at once but ran into "Foreign Key Constraint" errors. I solved this by strictly ordering the execution so that the dimension tables were populated before the fact table attempted to reference them.


