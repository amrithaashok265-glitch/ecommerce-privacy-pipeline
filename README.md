# 🛡️ End-to-End Enterprise Data Platform & Privacy Engineering Pipeline

This repository contains a production-ready data engineering framework that implements scalable ETL pipelines, relational data modeling, and robust data privacy controls. The architecture adheres to global compliance standards (like GDPR and HIPAA) by securing Personally Identifiable Information (PII) at rest and enforcing strict access boundaries between downstream data consumers.

---

##  My Project Journey & Engineering Decisions

When I started building this pipeline, my goal was to transform raw data into a clean, secure database. Along the way, I noticed gaps that weren't explicitly requested, but were necessary to make this platform enterprise-grade. Here is what I implemented and why:

### 1. Proactive Country & Phone Standardization (Going Beyond the Requirements)
* **The Problem:** When analyzing the case study, I noticed that all the sample data only showed US phone numbers. Because of this, a basic implementation would have just hardcoded "US" rules into the cleaning logic. But I stopped and thought: *What if our business expands tomorrow and we get a UAE number or an Indian number?* Hardcoded US logic would completely break or corrupt international data. Furthermore, the raw country fields were messy and inconsistent (like `"USA"`, `"uae "`, or `"India"`).
* **My Solution:** I took the initiative to build a dynamic, future-proof solution. Instead of hardcoding a single country, I updated the logic to dynamically read the country field first. I built the `normalize_country` function to strip out accidental spaces, fix capitalization, and map inputs to standard ISO 2-letter codes (like `US`, `AE`, `IN`). 
* **The Impact:** Now, the pipeline reads the standardized country code first and automatically passes it into the phone validation logic (`to_e164`). This allows the system to instantly know whether to format the phone number as a US, UAE, or Indian number dynamically. It turns a rigid script into a highly scalable, global data pipeline!

### 2. Learning the Difference Between Hashing and Encryption
This project helped me truly understand how to handle data privacy in two completely different ways based on who needs the data:
* **For Analytics:** I learned that data analysts don't need to know a customer's real phone number to count their orders or calculate their **Lifetime Value (LTV)**. So, I used **SHA-256 Hashing with a Salt**. It creates a permanent, unreadable fingerprint that lets them join tables safely without risking anyone's privacy.
* **For Operations:** I realized that the delivery system *does* need the real number to send an SMS text. For this, I used **AES-256 (Fernet) Encryption** because it can be safely decoded back into plain text in-memory right when the script runs, and then immediately discarded.

### 3. Key Management & Cryptographic Security
* **The Approach:** To ensure enterprise-grade security, I implemented a strict Key Management strategy. The symmetric AES-256 `ENCRYPTION_KEY` used by the Fernet client is never hardcoded into the scripts or saved into the repository. 
* **The Solution:** Instead, the key is fed into the runtime memory using environment configurations. The SHA-256 salt value is managed identically. 
* **Why it matters:** This ensures that even if our source code repository is leaked or accessed by unauthorized users, the customer data remains completely scrambled and safe because the keys to open it live outside the application codebase.

### 4. The Power of Unit Testing
* **What I Did:** I created a separate `unit_test_validation.py` script filled with hardcoded edge cases (like testing how the code handles dummy text or bad phone formats). 
* **What I Learned:** This taught me the value of **Unit Testing**. By checking my Python formulas with fake data *before* connecting them to the actual Excel files or the SQL database, I could instantly see if my logic was broken without messing up our production database structure.

### 5. Splitting the Code for Security
* **My Approach:** Instead of putting everything into one massive Python file, I intentionally separated the **Pipeline (ETL)**, the **Testing Suite**, and the **Operational Service** into their own files.
* **Why it matters:** This taught me the *Principle of Least Privilege*. The code that sends SMS notifications shouldn't have the power to alter database tables or look at the entire customer list. Keeping them separate keeps the whole application lightweight and highly secure.

---

##  Installation & Deployment Runbook
* **pipeline.py (The Ingestion Engine):** This is the heart of the project. It handles the ETL process—reading the raw Excel sheets, running the data cleaning functions (like fixing the country names), executing the SHA-256 hashing and AES encryption, and saving everything into the SQLite database.

* **schema.sql (The Database Blueprint):** This file contains the raw SQL commands (DDL) used to build the database. It defines the layout of our physical tables (customers and orders) and sets up the secure database view (v_analytics_customer_orders).

* **unit_test_validation.py (The Quality Assurance Suite):** This is our Unit Testing file. It contains isolated tests filled with fake, messy data to verify that our country-cleaning and phone-standardization logic work flawlessly before we run them on live production data.

* **data_quality_check.py (The Reporting Engine):** This script acts as our verification and reporting tool. It runs queries against the database to confirm that the PII data is hidden properly and automatically calculates our final Customer Lifetime Value (LTV) business report.

* **operational_service.py (The Live Operational Tool):** This simulates a real-world backend service used by a delivery team. It securely queries a single customer record and uses our encryption keys to decrypt the phone number strictly in-memory so an SMS notification can be sent.

* **customer_table.xlsx & order_table.xlsx (The Raw Datasets):** These are the source Excel files provided in the case study that contain our uncleaned customer profiles and transactional transaction sheets.

* **.env (Environment Secrets File):** This file stores your highly sensitive ENCRYPTION_KEY and your cryptographic SALT value. By separating these configurations into a private text file, you ensure your secret keys are injected directly into the application's memory at runtime without ever leaking into your public code repositories.
---

## Step's to generate keys and run the architecture.

* **Step 1: Generate Custom Cryptographic Encryption Key**
Run this command in your terminal to create your symmetric AES-256 key:

   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

   Copy the long random text string that pops out on the screen, store that value in the ENCRYPTION_KEY in .env file, and save.

* **Step 2: Run Privacy Engineering Data Pipeline**
    
    python pipeline.py

* **Step 3: Test the Operational Verification Layer**

    python operational_service.py

* **Step 4: Test Unit Testing**

    python unit_test_validation.py

* **Step 5: Data Quality Check**

    python data_quality_check.py
    

---

##  Platform Architecture & Data Flow

The platform separates responsibilities into three distinct architectural layers to minimize data exposure risks:

1. **Ingestion & Standardization Layer:** Consumes raw business datasets (Excel format), fixes messy inconsistencies, and structures values into clean, compliant formats (ISO country tracking and E.164 phone schemas).
2. **Analytical Layer (Masked):** Exposes a virtual SQL database view containing irreversible SHA-256 hashes for data analytics and metric tracking (e.g., Customer Lifetime Value) without exposing actual contact numbers.
3. **Operational Layer (Decoupled):** Implements an isolated application-layer execution service that leverages symmetric AES-256 (Fernet) decryption strictly in-memory for real-time transactional utility (e.g., dispatching SMS shipping updates).

```text
 [Messy Excel Sources] 
         │
         ▼
 ┌────────────────────────────────────────────────────────┐
 │            Python Ingestion Engine (ETL)               │ ──> [Automated Unit Test Suite]
 └────────────────────────────────────────────────────────┘
         │
         ├─── Irreversible SHA-256 Hashing + Salt
         └─── Reversible AES-256 Symmetric Encryption
         │
         ▼
 ┌────────────────────────────────────────────────────────┐
 │           SQLite Physical Layer (Base Tables)          │
 └────────────────────────────────────────────────────────┘
         │                                       │
         ▼ (SQL View Boundary)                   ▼ (Programmatic Runtime Access)
 ┌───────────────────────────────┐       ┌───────────────────────────────┐
 │       Analytics Layer         │       │       Operational Layer       │
 │   (v_analytics_customer_orders)│      │    (In-Memory PII Decryption) │
 └───────────────────────────────┘       └───────────────────────────────┘
         │                                       │
         ▼                                       ▼
  [LTV Business Reports]                 [Transient SMS Notification API]