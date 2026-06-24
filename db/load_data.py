import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# SQLAlchemy is a library that lets pandas talk to PostgreSQL
# We build a connection string from our .env variables

# def get_engine():
#     return create_engine(f"postgresql+psycopg2://postgres:postgres@localhost:5433/nl2sql_db")

# def get_engine():
#     user = os.getenv("DB_USER")
#     password = os.getenv("DB_PASSWORD")
#     host = os.getenv("DB_HOST")
#     port = os.getenv("DB_PORT")
#     dbname = os.getenv("DB_NAME")
#     return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")


def get_engine():
    user = os.getenv("VECTOR_DB_USER")
    password = os.getenv("VECTOR_DB_PASSWORD")
    host = os.getenv("VECTOR_DB_HOST")
    port = os.getenv("VECTOR_DB_PORT")
    dbname = os.getenv("VECTOR_DB_NAME")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

def load_table(engine, filepath, table_name, parse_dates=None):
    print(f"Loading {table_name}...")
    df = pd.read_csv(filepath, parse_dates=parse_dates)
    # if_exists='replace' drops and recreates the table each time
    # index=False means don't add a pandas row number column
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"  Done — {len(df)} rows loaded into {table_name}")

if __name__ == "__main__":
    engine = get_engine()

    load_table(engine, 'data/olist_orders_dataset.csv', 'orders',
               parse_dates=['order_purchase_timestamp', 'order_approved_at',
                            'order_delivered_carrier_date',
                            'order_delivered_customer_date',
                            'order_estimated_delivery_date'])

    load_table(engine, 'data/olist_customers_dataset.csv', 'customers')
    load_table(engine, 'data/olist_order_items_dataset.csv', 'order_items')
    load_table(engine, 'data/olist_products_dataset.csv', 'products')
    load_table(engine, 'data/olist_sellers_dataset.csv', 'sellers')
    load_table(engine, 'data/olist_order_payments_dataset.csv', 'order_payments')
    load_table(engine, 'data/olist_order_reviews_dataset.csv', 'order_reviews')
    load_table(engine, 'data/product_category_name_translation.csv', 'category_translation')

    print("\nAll tables loaded successfully!") 