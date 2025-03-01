import sqlite3
import pandas as pd

# Path to the SQLite database
db_path = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4\violations.db"

# Step 1: Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Query the violations table for Moderate Risk violations on or after 2016-02-23
query = """
    SELECT business_id, date
    FROM violations
    WHERE risk_category = 'Moderate Risk'
    AND date >= '2016-02-23'
"""

# Step 3: Execute the query and fetch results
df_violations = pd.read_sql_query(query, conn)

# Step 4: Close the database connection
conn.close()

# Print first few rows to verify
print(df_violations.head())

# Save to CSV for future use (optional)
df_violations.to_csv("moderate_risk_violations.csv", index=False)

# Print total records
print(f"Total Moderate Risk violations on or after 2016-02-23: {len(df_violations)}")
