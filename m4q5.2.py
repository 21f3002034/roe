import os
import fitz  # pymupdf
import sqlite3
import pandas as pd

# File path to the folder containing PDF files
pdf_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(pdf_folder, "violations.db")

### Step 1: Extract business_id and date from inspections-*.pdf ###
inspection_data = set()

for filename in os.listdir(pdf_folder):
    if filename.startswith("inspections-") and filename.endswith(".pdf"):
        try:
            # Extract date from filename (e.g., inspections-2016-03-15.pdf -> 2016-03-15)
            date = filename.replace("inspections-", "").replace(".pdf", "")

            pdf_path = os.path.join(pdf_folder, filename)
            doc = fitz.open(pdf_path)

            for page in doc:
                text = page.get_text("text")  # Extract text as a string
                lines = text.split("\n")  # Split into lines

                for line in lines:
                    parts = line.strip().split()  # Split line into words
                    if len(parts) >= 1:
                        business_id = parts[0].strip()

                        if business_id.isdigit():  # Ensure valid business ID
                            inspection_data.add((business_id, date))

        except Exception as e:
            print(f"Error processing {filename}: {e}")

### Step 2: Extract business_id and date from violations.db (Moderate Risk, date >= 2016-02-23) ###
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = """
    SELECT business_id, date
    FROM violations
    WHERE risk_category = 'Moderate Risk' AND date >= '2016-02-23'
"""

df_violations = pd.read_sql_query(query, conn)
conn.close()

# Convert violations to a set for fast lookup
violation_data = set(df_violations.itertuples(index=False, name=None))

### Step 3: Count violations not found in inspections data ###
violations_without_inspection = [entry for entry in violation_data if entry not in inspection_data]

# Print the result
print("Number of violations without an inspection:", len(violations_without_inspection))
