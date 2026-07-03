import os
import sqlite3
import hashlib
import pandas as pd
import phonenumbers
from phonenumbers import PhoneNumberFormat
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
HASH_SALT = os.getenv("HASH_SALT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "customer_data.db")

if not ENCRYPTION_KEY or not HASH_SALT:
    raise ValueError(" Missing environment configuration details in your local .env file!")

fernet = Fernet(ENCRYPTION_KEY.encode())

def normalize_country(country):
    """Normalizes raw input strings into clean ISO-2 alpha country codes."""
    if country is None or pd.isna(country):
        return "UNKNOWN"
    country = str(country).strip().upper()
    mapping = {
        "USA": "US", "US": "US",
        "UAE": "AE", "UAW": "AE",
        "INDIA": "IN", "IND": "IN", "IN": "IN"
    }
    return mapping.get(country, "UNKNOWN")

def to_e164(raw, region):
    """Transforms global phone strings into clean international standard formats."""
    try:
        parsed = phonenumbers.parse(str(raw), region)
        return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
    except:
        return None

def hash_phone(clean_phone, salt):
    """Generates an irreversible cryptographic hash value used as an analytics join key."""
    if not clean_phone: return "INVALID_PHONE"
    return hashlib.sha256((clean_phone + salt).encode()).hexdigest()

def encrypt_phone(clean_phone, fernet_client):
    """Encrypts cleartext data using symmetric AES-256 algorithms for operations."""
    if not clean_phone: return "INVALID_PHONE"
    return fernet_client.encrypt(clean_phone.encode()).decode()

def initialize_database():
    """Reads schema definitions to build relational tables and structural views."""
    conn = sqlite3.connect(DATABASE_NAME)
    with open("schema.sql", "r") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    print(" Database schemas and analytic views initialized successfully.")

def run_pipeline():
    """Executes the operational ETL orchestration sequence."""
    print(" Initiating data engineering security pipeline execution...")
    
    # 1. Ingest customer datasets and apply clean-room transformations
    customer_df = pd.read_excel("data/customer_table.xlsx")
    customer_df["country_std"] = customer_df["country"].apply(normalize_country)
    customer_df["phone_e164"] = customer_df.apply(
        lambda row: to_e164(row["raw_phone_number"], row["country_std"]), axis=1
    )
    
    # Apply security engineering layers onto clean datasets
    customer_df["hashed_phone"] = customer_df["phone_e164"].apply(lambda x: hash_phone(x, HASH_SALT))
    customer_df["encrypted_phone"] = customer_df["phone_e164"].apply(lambda x: encrypt_phone(x, fernet))
    
    # Select the columns directly matching our database blueprints
    final_customers = customer_df[[
        "customer_id", 
        "customer_name", 
        "country", 
        "country_std", 
        "hashed_phone", 
        "encrypted_phone"
    ]]
    
    # 2. Ingest transaction datasets
    orders_df = pd.read_excel("data/order_table.xlsx")
    
    # 3. Load processed entities directly into secure storage targets
    conn = sqlite3.connect(DATABASE_NAME)
    final_customers.to_sql("customers", conn, if_exists="append", index=False)
    orders_df.to_sql("orders", conn, if_exists="append", index=False)
    conn.close()
    
    print(" Secure data pipelines processed and loaded completely!")

if __name__ == "__main__":
    initialize_database()
    run_pipeline()