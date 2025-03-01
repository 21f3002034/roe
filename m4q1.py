import os
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

# Path to dataset
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(html_folder, "violations.db")

# Step 1: Extract business_id for postal code 94110 from HTML files
business_ids_94110 = set()

for filename in os.listdir(html_folder):
    if filename.startswith("biz-") and filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            # Loop through all tables
            for table in soup.find_all("table"):
                rows = table.find_all("tr")

                business_id = None
                postal_code = None

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        for i in range(len(cols) - 1):
                            if cols[i].text.strip() == "business_id":
                                business_id = cols[i + 1].text.strip()
                            if cols[i].text.strip() == "postal_code":
                                postal_code = cols[i + 1].text.strip()

                if business_id and postal_code == "94110":
                    business_ids_94110.add(business_id)

# Step 2: Query violations.db for Moderate Risk violations on a Monday
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = """
    SELECT business_id, date 
    FROM violations 
    WHERE risk_category = 'Moderate Risk'
    AND business_id IN ({})
""".format(",".join(["?"] * len(business_ids_94110)))

cursor.execute(query, tuple(business_ids_94110))
records = cursor.fetchall()
conn.close()

# Step 3: Count violations per business_id that happened on a Monday
violation_counts = {}

def is_monday(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").weekday() == 0  # Monday is 0
    except ValueError:
        return False

for biz_id, date in records:
    if is_monday(date):
        violation_counts[biz_id] = violation_counts.get(biz_id, 0) + 1

# Step 4: Sum all violations for postal code 94110
total_violations_94110 = sum(violation_counts.values())

print("Total Moderate Risk violations on Mondays for postal code 94110:", total_violations_94110)
