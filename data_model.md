# 🗺️ E-Commerce Privacy Data Model Architecture (ERD & Views)

This document maps out the complete relationship structure of our data platform, showing the physical base tables alongside the logical access boundaries designed for different downstream business teams.

```mermaid
erDiagram
    %% --- Relationships Between Base Tables ---
    CUSTOMERS ||--o{ ORDERS : "places"

    %% --- Logical Lineage (How data flows into views) ---
    CUSTOMERS ||--|| V_ANALYTICS_VIEW : "projects into"
    ORDERS ||--o{ V_ANALYTICS_VIEW : "joins into"
    CUSTOMERS ||--|| OPERATIONAL_LOGICAL_VIEW : "decrypts into via Python runtime"

    %% --- Physical Storage Layer ---
    CUSTOMERS {
        int customer_id PK
        string customer_name
        string country
        string country_std
        string hashed_phone "SHA-256 (Analytical Tracking Key)"
        string encrypted_phone "AES-256 (Ciphertext Token)"
    }

    ORDERS {
        int order_id PK
        int customer_id FK
        string order_date
        float order_amount
        string delivery_status
        string delivery_address
    }

    %% --- Secure Analytics Boundary Layer ---
    V_ANALYTICS_VIEW {
        int customer_id
        string customer_name
        string country_std
        string hashed_phone "SHA-256 ONLY (Encrypted Phone Stripped)"
        int order_id
        float order_amount "Used for LTV Analysis"
        string order_date
    }

    %% --- Isolated Operational Layer ---
    OPERATIONAL_LOGICAL_VIEW {
        int customer_id
        string customer_name
        string cleartext_phone "Decrypted E.164 (In-Memory Only)"
        string delivery_status
        string delivery_address
    }