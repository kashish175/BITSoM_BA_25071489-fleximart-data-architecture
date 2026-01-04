# ------Task 1.1: ETL Pipeline Implementation-------


import pandas as pd
import os
from sqlalchemy import text
from sqlalchemy import create_engine
import mysql.connector

# 1. Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go UP one level to the root where the 'Data' folder lives
root_dir = os.path.dirname(script_dir)
data_folder = os.path.join(root_dir, "Data")

# 1. Initialize report metrics (The Scoreboard)
report_metrics = {
    "records_processed": {}, # To store counts for Customers, Products, Sales
    "duplicates_removed": 0,
    "missing_values_handled": 0,
    "records_loaded": {},  # To store counts of customers, products, orders and order_item loaded
    "total_records_loaded": 0,
    "missing_values_removed" : 0
}

# ------**Step 1: Extracting data from CSV files **-------
print("Starting Extracting Phase...")

try:
    df_customers = pd.read_csv(os.path.join(data_folder, "customers_raw.csv"))
    df_products = pd.read_csv(os.path.join(data_folder, "products_raw.csv"))
    df_sales = pd.read_csv(os.path.join(data_folder, "sales_raw.csv"))
    
    print("Files extracted successfully!")

    report_metrics["records_processed"]["customers"] = len(df_customers)
    report_metrics["records_processed"]["products"] = len(df_products)
    report_metrics["records_processed"]["sales"] = len(df_sales)

    
except FileNotFoundError as e:
    print(f"Error: Could not find file. {e}")

print(df_customers.head(),
      df_products.head(),
      df_sales.head())
print("Extracting Phase Ends....")


#---------** Step2 : Transforming and Cleaning the data**---------------
print("Starting Transformation Phase...")

#------ Transform and Clean Customers Data-------
print("Transforming and Cleaning Customers Data.....")

# 1. Remove duplicate rows
print("Removing duplicate rows........")
before_dup = len(df_customers)
df_customers = df_customers.drop_duplicates()
report_metrics["duplicates_removed"] += (before_dup - len(df_customers))

# 2. Handle missing emails
print("Assigning unique values to missing emails.........")
#  Identify where emails are missing
missing_email_mask = df_customers['email'].isna()
num_missing = missing_email_mask.sum()
report_metrics["missing_values_handled"] += num_missing

# Create a list of unique placeholders: no_email_0@fleximart.com, no_email_1@fleximart.com, etc.
unique_placeholders = [f'no_email_{i}@fleximart.com' for i in range(num_missing)]

# Fill only the missing spots with these unique values
df_customers.loc[missing_email_mask, 'email'] = unique_placeholders

print(f"Successfully assigned {num_missing} unique placeholder emails!")

# 3. Standardize phone formats
print("Standardizing phone formats........")
def standardize_phone(phone):
    # Convert to string and remove symbols
    clean_p = str(phone).replace('+', '').replace('-', '')
    
    # Remove leading '0' or '91' if they exist to get to the core 10 digits
    if clean_p.startswith('91') and len(clean_p) > 10:
        clean_p = clean_p[2:]
    elif clean_p.startswith('0'):
        clean_p = clean_p[1:]
    
    # Return the standardized string
    return f"+91-{clean_p[-10:]}"

# Apply the function to the 'phone' column
df_customers['phone'] = df_customers['phone'].apply(standardize_phone)

# Let's check the results
print(df_customers[['first_name', 'phone']].head())

# 4. Convert date formats to YYYY-MM-DD
print("Converting date formats to YYYY-MM-DD ......... ")
df_customers['registration_date'] = pd.to_datetime(df_customers['registration_date'], format='mixed', errors='coerce')

# Now convert to the final string format YYYY-MM-DD
df_customers['registration_date'] = df_customers['registration_date'].dt.strftime('%Y-%m-%d')

# 5. Add surrogate keys (auto-incrementing IDs)
print("Adding surrogate key..........")
# Add a surrogate key (auto-incrementing ID) starting from 1
df_customers.insert(0, 'id', range(1, 1 + len(df_customers)))

#  final cleaned customer data
print(df_customers.head())

print("Transformation and Cleaning of Customers Data Completed.....")

#------ Transform Products Data-------
print("Transforming and Cleaning Products Data.....")

# 1. Remove duplicates
print("Removing duplicate rows........")
before_dup = len(df_products)
df_products = df_products.drop_duplicates()
report_metrics["duplicates_removed"] += (before_dup - len(df_products))

# Count missing values for Price and Stock
missing_prices = df_products['price'].isna().sum()
missing_stock = df_products['stock_quantity'].isna().sum()
print("Missing prices=" ,missing_prices)
print("Missing stock=",missing_stock )

# Update the report metrics total
report_metrics["missing_values_handled"] += (missing_prices + missing_stock)

# 2. Handle missing values
# Handling missing prices (Category-based MEDIAN imputation)
print("Imputing missing prices using category medians...")

# Group by category and fill missing prices with the MEDIAN of that category
df_products['price'] = df_products['price'].fillna(
    df_products.groupby('category')['price'].transform('median')
)

# Final safety check: if a whole category is empty, use the global median
global_median = df_products['price'].median()
df_products['price'] = df_products['price'].fillna(global_median).round(2)

# Handling missing stocks values (Assuming no stock available for missing values)
print("Assigning 0 to the missing stocks......")
df_products['stock_quantity'] = df_products['stock_quantity'].fillna(0)

# 3. Standardize categories (e.g., electronics -> Electronics)
print("Standarizing Category.....")
df_products['category'] = df_products['category'].str.capitalize()

# 4. Add a surrogate key (auto-incrementing ID)
print("Adding surrogate key..........")
df_products.insert(0, 'id', range(1, 1 + len(df_products)))

#final cleaned products data
print(df_products.head())

print("Transformation and Cleaning of Products Data Completed.....")

#------ Transform Sales Data-------
print("Transforming and Cleaning Sales Data.....")

# 1. Remove duplicates
print("Removing duplicate rows........")
before_dup = len(df_sales)
df_sales = df_sales.drop_duplicates()
report_metrics["duplicates_removed"] += (before_dup - len(df_sales))

# Count rows before dropping
before_drop = len(df_sales)

# 2. Drop rows where critical IDs (Foreign Keys) are missing
print("Dropping rows with missing product and customer ids........")
df_sales = df_sales.dropna(subset=['customer_id', 'product_id'])

#  Calculate how many were removed and add to report metrics
rows_removed = before_drop - len(df_sales)
report_metrics["missing_values_removed"] += rows_removed

# 3. Standardize dates
print("Converting date formats to YYYY-MM-DD ......... ")
df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'], format='mixed', errors='coerce')
df_sales['transaction_date'] = df_sales['transaction_date'].dt.strftime('%Y-%m-%d')

# 4. Add a surrogate key (auto-incrementing ID)
print("Adding surrogate key..........")
df_sales.insert(0, 'id', range(1, 1 + len(df_sales)))

#final cleaned sales data
print(df_sales.head())

print("Transformation and Cleaning of Sales Data Completed.....")

print("Transformation Phase Ends.........")
print("Data cleaning complete.....")


# ------Customers Data for Loading---------

# for loading customer data in MySQL Workbench
# Rename columns to map the text-based ID to a reference column 
# and the numeric surrogate key to the primary key
df_customers: pd.DataFrame = df_customers.rename(columns={
    'customer_id': 'external_id',
    'id': 'customer_id'
})

#  final version of the customer data for loading
customers_final = df_customers[['customer_id', 'first_name', 'last_name', 
                                'email', 'phone', 'city', 'registration_date']]

print("Clean customers data for 'Customers Table")
print(customers_final.head())

#------ Products Data for Loading ----------

# for loading products data in MySQL Workbench
# Rename columns to map the text-based ID to a reference column 
# and the numeric surrogate key to the primary key
df_products: pd.DataFrame = df_products.rename(columns={
    'product_id': 'external_id',
    'id': 'product_id'
})

# final version of the products data for loading
products_final= df_products[['product_id','product_name',
                              'category', 'price', 'stock_quantity']]
print("Clean products data for 'Products Table'")
print(products_final.head())

#-------- Sales Data for Loading -----------

# for loading sales data in MySQL Workbench
# Rename columns to map the text-based ID to a reference column 
# and the numeric surrogate key to the primary key
df_sales: pd.DataFrame = df_sales.rename(columns={
    'transaction_id': 'id',
    'id': 'transaction_id'
})

# 1. Merge sales with customers to get the numeric customer_id
# We match 'customer_id' from sales to 'external_id' (the old C001) in customers
df_sales = pd.merge(
    df_sales, 
    df_customers[['customer_id', 'external_id']], 
    left_on='customer_id', 
    right_on='external_id', 
    suffixes=('_old', '')
)

# 1. Merge sales with products to get the numeric products_id
# We match 'product_id' from sales to 'external_id' (the old P001) in products
df_sales = pd.merge(
    df_sales, 
    df_products[['product_id', 'external_id']], 
    left_on='product_id', 
    right_on='external_id', 
    suffixes=('_old', '')
)

df_sales = df_sales.drop(columns=['customer_id_old', 'product_id_old', 'external_id_old', 'external_id','id'])

# 1. Calculate the total_amount for the orders table
df_sales['total_amount'] = df_sales['quantity'] * df_sales['unit_price']

# 2.rename columns to match the 'orders' table
df_sales: pd.DataFrame = df_sales.rename(columns={'transaction_date': 'order_date',
                                                   'transaction_id':'order_id'})

# final version of the sales/orders data for loading
orders_final = df_sales[['order_id', 'customer_id',  'order_date',  'total_amount',  'status']]
print("Clean sales data for 'Orders Table' " )
print(orders_final.head())

#--------- Order item Dataframe for Loading ---------

# Create the order_items DataFrame as a completely independent object
order_items_final = df_sales[['order_id', 'product_id', 'quantity', 'unit_price']].copy()

# adding order item id column
# Create a sequence from 1 to the length of the DataFrame
order_items_final['order_item_id'] = range(1, len(order_items_final) + 1)

# Ensure order_item_id is the first column for clarity
cols = ['order_item_id'] + [c for c in order_items_final if c != 'order_item_id']
order_items_final = order_items_final[cols]

#  adding subtotal column
order_items_final['subtotal'] = order_items_final['quantity'] * order_items_final['unit_price']

print ("Clean data for 'Order_item Table' ")
print(order_items_final.head())


import os
from sqlalchemy import create_engine

# 1. Setup your connection details
user = "root"
host = "localhost"
port = "3306"
db = "fleximart"
password = os.getenv("MYSQL_PASSWORD") 
if password is None:
    print(" ERROR: Environment variable 'MYSQL_PASSWORD' not found. Please set it in Windows.")

# 2. Define the connection URL 
connection_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"

# 3. Create the engine
engine = create_engine(connection_url)

# 4. A quick test to ensure the bridge is working
try:
    with engine.connect() as connection:
        print("Successfully connected to the FlexiMart database! ")
except Exception as e:
    print(f"Connection failed. Error: {e}")

# ----------** STEP 3: Loading data into MySQL **-----------
print("Starting the Load phase...")

try:
    with engine.connect() as conn:
        print("Clearing old data safely...")
        # Disable foreign key checks to allow truncating linked tables
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("TRUNCATE TABLE order_items;"))
        conn.execute(text("TRUNCATE TABLE orders;"))
        conn.execute(text("TRUNCATE TABLE customers;"))
        conn.execute(text("TRUNCATE TABLE products;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        conn.commit()
         
    # Now upload the cleaned dataframes
    customers_final.to_sql('customers', con=engine, if_exists='append', index=False)
    print(f"Uploaded {len(customers_final)} Customers.")
    report_metrics["records_loaded"]["customers"] = len(customers_final)

    products_final.to_sql('products', con=engine, if_exists='append', index=False)
    print(f"Uploaded {len(products_final)} Products.")
    report_metrics["records_loaded"]["products"] = len(products_final)
   

    orders_final.to_sql('orders', con=engine, if_exists='append', index=False)
    print(f"Uploaded {len(orders_final)} Orders.")
    report_metrics["records_loaded"]["orders"] = len(orders_final)
   

    order_items_final.to_sql('order_items', con=engine, if_exists='append', index=False)
    print(f"Uploaded {len(order_items_final)} Order Items.")
    report_metrics["records_loaded"]["order_items"] = len(order_items_final)

    # Update final metric for the report
    report_metrics["total_records_loaded"] = len(customers_final) + len(products_final) + \
                                       len(orders_final) + len(order_items_final)
    
    print(f"\nAll data successfully loaded! \nTotal records: {report_metrics['total_records_loaded']} ")

except Exception as e:
    print(f" Load Error: {e}")


  # ---------**STEP 4: Generating the Quality report **--------
with open("part1-database-etl/data_quality_report.txt", "w") as f:
    f.write("=== FLEXIMART DATA QUALITY REPORT ===\n\n")
    
    # Records processed per file
    f.write("--- Records Processed Per File ---\n")
    for file_name, count in report_metrics["records_processed"].items():
        f.write(f"{file_name.capitalize()}: {count} records\n")
           
    f.write(f"\nDuplicates Removed: {report_metrics['duplicates_removed']}\n")
    f.write(f"Missing Values(Email, Price, Stock) Handled: {report_metrics['missing_values_handled']}\n")
    f.write(f"Missing Values (Customer_id, Product_id) Removed : {report_metrics['missing_values_removed']}\n\n")
    
    # Records loaded per file
    f.write("--- Records loaded Per File ---\n")
    for file_name, count in report_metrics["records_loaded"].items():
        f.write(f"{file_name.capitalize()}: {count} records\n")
    f.write(f"\nTotal Records Loaded Successfully: {report_metrics['total_records_loaded']}\n")
   
    f.write("\n=====================================")

print("Final report generated! ")


