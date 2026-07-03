import os
import sqlite3
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())
DATABASE_NAME = os.getenv("DATABASE_NAME", "customer_data.db")

def simulate_operational_notification(target_customer_id):
    """Pulls an encrypted data token and decrypts it back to raw string format at runtime."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, customer_name, encrypted_phone FROM customers WHERE customer_id = ?", (target_customer_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f" Matching profile context missing for ID: {target_customer_id}")
        return
        
    cust_id, name, encrypted_token = result
    decrypted_phone = fernet.decrypt(encrypted_token.encode()).decode()
    
    print("\n---  Operational Security Execution Verification ---")
    print(f"Operational ID Reference: {cust_id}")
    print(f"Customer Name:            {name}")
    print(f"Encrypted Target Token:   {encrypted_token[:30]}...")
    print(f"Decrypted Runtime Target: {decrypted_phone}")
    print("------------------------------------------------------\n")

if __name__ == "__main__":
    simulate_operational_notification(1)