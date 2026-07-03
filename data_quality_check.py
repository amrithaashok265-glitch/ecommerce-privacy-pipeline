import sqlite3
import pandas as pd

DATABASE_NAME = "customer_data.db"

def inspect_database():
    conn = sqlite3.connect(DATABASE_NAME)
    
    # Set pandas options to print nicely in the terminal
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    print("==================================================================")
    print(" 1. BASE TABLE: customers (Physical Storage Layer)")
    print("==================================================================")
    customers_df = pd.read_sql_query("SELECT * FROM customers;", conn)
    print(customers_df)
    
    print("\n==================================================================")
    print(" 2. BASE TABLE: orders (Transactional Fact Layer)")
    print("==================================================================")
    orders_df = pd.read_sql_query("SELECT * FROM orders;", conn)
    print(orders_df)
    
    print("\n==================================================================")
    print(" 3. SECURE VIEW: v_analytics_customer_orders (Analytics Layer)")
    print("==================================================================")
    view_df = pd.read_sql_query("SELECT * FROM v_analytics_customer_orders;", conn)
    print(view_df)
    conn.close()


def calculate_customer_ltv():
    conn = sqlite3.connect("customer_data.db")
    
    print("\n==================================================================")
    print("GENERATED REPORT: Customer Lifetime Value (LTV) from Secure View")
    print("==================================================================")
    
    ltv_query = """
    SELECT 
        customer_id,
        customer_name,
        country_std,
        SUM(order_amount) AS lifetime_value,
        COUNT(order_id) AS total_orders
    FROM v_analytics_customer_orders
    GROUP BY customer_id;
    """
    
    ltv_df = pd.read_sql_query(ltv_query, conn)
    print(ltv_df)
    conn.close()
    



if __name__ == "__main__":
    inspect_database()
    calculate_customer_ltv()
