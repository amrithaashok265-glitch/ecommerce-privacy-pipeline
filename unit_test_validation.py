import pandas as pd
from pipeline import normalize_country, to_e164, hash_phone

def test_pipeline_validation():
    print("Starting Data Engineering Validation Tests...\n")
    
    # --- Test 1: Country Standardization Logic ---
    print("1. Testing Country Normalization...")
    assert normalize_country("USA") == "US"
    assert normalize_country("uae ") == "AE"  # Tests case and whitespace handling
    assert normalize_country("India") == "IN"
    assert normalize_country("InvalidCountry") == "UNKNOWN"
    print(" Country normalization rules passed!")

    # --- Test 2: Phone Standardization (E.164) ---
    print("\n2. Testing Phone Format Validation...")
    # Valid US Number with country code
    assert to_e164("+1 555-123-4567", "US") == "+15551234567"
    # Valid UAE Number
    assert to_e164("0501234567", "AE") == "+971501234567"
    # Completely broken phone number string
    assert to_e164("not-a-phone-number", "US") is None
    print(" E.164 phone validation rules passed!")

    # --- Test 3: Anonymization Integrity ---
    print("\n3. Testing Hash Consistency...")
    salt = "TestSalt123!"
    hash1 = hash_phone("+15551234567", salt)
    hash2 = hash_phone("+15551234567", salt)
    
    # Deterministic test: The same input must always produce the same hash
    assert hash1 == hash2
    # Edge case test: Invalid inputs should fail gracefully
    assert hash_phone(None, salt) == "INVALID_PHONE"
    print("  Cryptographic hashing stability passed!")

    print("\nALL PIPELINE VALIDATION TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    test_pipeline_validation()