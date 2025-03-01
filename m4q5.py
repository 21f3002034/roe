import os
import pdfplumber
import sqlite3
import pandas as pd
from datetime import datetime

# File path to the folder containing PDF files
pdf_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(pdf_folder, "violations.db")

# Define the cutoff date for filtering
cutoff_date = datetime.strptime("2016-02-23", "%Y-%m-%d")

### Step 1: Extract business_id and date from inspections-*.pdf ###
inspection_data = []

for filename in os.listdir(pdf_folder):
    if filename.startswith("inspections-") and filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table[1:]:  # Skip header row
                        try:
                            business_id = row[0].strip()  # First column: business_id
                            date_str = row[1].strip()  # Second column: date

                            # Convert to datetime for proper comparison
                            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                            # Only keep records on or after the cutoff date
                            if business_id.isdigit() and date_obj >= cutoff_date:
                                inspection_data.append([business_id, date_str])

                        except (IndexError, AttributeError, ValueError):
                            continue  # Skip invalid rows

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

# Convert violation dates to datetime format for proper comparison
df_violations["date"] = pd.to_datetime(df_violations["date"], format="%Y-%m-%d")

# Convert violations to a list of lists for comparison
violation_data = df_violations.astype(str).values.tolist()

print(inspection_data[0])
print (violation_data[0])
### Step 3: Count violations not found in inspections data ###
violations_without_inspection = [entry for entry in violation_data if entry not in inspection_data]

# Print the result
print("Number of violations without an inspection:", len(violations_without_inspection))
