import os
import pdfplumber
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# File paths
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(html_folder, "violations.db")

### Step 1: Scrape business_id and postal_code from HTML ###
biz_data = []

for filename in os.listdir(html_folder):
    if filename.startswith("biz-") and filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            for table in soup.find_all("table"):
                rows = table.find_all("tr")

                business_id = None
                postal_code = None

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        for i in range(len(cols) - 1):
                            key = cols[i].text.strip()
                            value = cols[i + 1].text.strip()

                            if key == "business_id":
                                business_id = value
                            elif key == "postal_code":
                                postal_code = value

                if business_id and postal_code:  # Drop missing values
                    biz_data.append([business_id, postal_code])

# Convert to DataFrame
df_biz = pd.DataFrame(biz_data, columns=["business_id", "postal_code"])

### Step 2: Scrape business_id, date, and score from inspections-*.pdf ###
inspection_data = []

for filename in os.listdir(html_folder):
    if filename.startswith("inspections-") and filename.endswith(".pdf"):
        pdf_path = os.path.join(html_folder, filename)

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table[1:]:  # Skip header row
                        try:
                            business_id = row[0].strip()  # First column: business_id
                            date = row[1].strip()  # Second column: date
                            score = row[2].strip()  # Third column: score

                            if business_id.isdigit() and date and score.isdigit():
                                inspection_data.append([business_id, date, int(score)])

                        except (IndexError, AttributeError, ValueError):
                            continue  # Skip invalid rows

# Convert inspection data to DataFrame
df_inspections = pd.DataFrame(inspection_data, columns=["business_id", "date", "score"])

# Drop missing values
df_inspections.dropna(inplace=True)
print(df_inspections.head())
### Step 3: Extract business_id, date, and description from violations.db ###
conn = sqlite3.connect(db_path)
query = """
    SELECT business_id, date, description 
    FROM violations 
    WHERE description LIKE '%water%' 
        OR description LIKE '%unapproved%' 
        OR description LIKE '%moderate%' 
        OR description LIKE '%facilities%' 
        OR description LIKE '%unsanitary%'
"""
df_violations = pd.read_sql_query(query, conn)
conn.close()

# Drop missing values
df_violations.dropna(inplace=True)

### Step 4: Join all three datasets ###
# Convert columns to string for merging
df_biz["business_id"] = df_biz["business_id"].astype(str)
df_inspections["business_id"] = df_inspections["business_id"].astype(str)
df_inspections["date"] = df_inspections["date"].astype(str)
df_violations["business_id"] = df_violations["business_id"].astype(str)
df_violations["date"] = df_violations["date"].astype(str)
print(df_violations.head(),end="\n\n")
print(df_inspections.head(),end="\n\n")    
# Join violations with inspections on (business_id, date)
df_merged = pd.merge(df_violations, df_inspections, on=["business_id", "date"])

# Join with business data on business_id
df_final = pd.merge(df_merged, df_biz, on="business_id")
print(df_final.head(),end="\n\n")
### Step 5: Filter where score >= 80 ###
df_filtered = df_final[df_final["score"] >= 80]

df_filtered = df_filtered.dropna()
df_filtered.to_csv("m4q6.csv", index=False)
### Step 6: Find businesses in postal code 94110 ###
df_94110 = df_filtered[df_filtered["postal_code"] == "94110"]
df_94110 = df_94110.dropna()
# Count the number of businesses
df_94110.to_csv("m4q6_94110.csv", index=False)
unique_businesses = df_94110["business_id"].nunique()

# Print the result
print("Number of businesses in postal code 94110 meeting the conditions:", unique_businesses)
