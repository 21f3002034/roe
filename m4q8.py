import os
import pdfplumber
import sqlite3
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from sklearn.linear_model import LinearRegression

# File paths
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"

### Step 1: Scrape business_id, date, and score from inspections-*.pdf ###
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

### Step 2: Scrape business_id and postal_code from biz-*.html ###
target_postal_codes = {"94121", "94133", "94116", "94103", "94117"}
business_data = []

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

                if business_id and postal_code in target_postal_codes:
                    business_data.append([business_id, postal_code])

# Convert to DataFrame
df_business = pd.DataFrame(business_data, columns=["business_id", "postal_code"])

# Drop missing values
df_business.dropna(inplace=True)

### Step 3: Join inspections data with HTML data on business_id ###
df_inspections["business_id"] = df_inspections["business_id"].astype(str)
df_business["business_id"] = df_business["business_id"].astype(str)

df_merged = pd.merge(df_inspections, df_business, on="business_id")

### Step 4: Convert Dates into Numerical Format ###
df_merged["date"] = pd.to_datetime(df_merged["date"], format="%Y-%m-%d")

# Convert dates to numerical format (days since earliest inspection)
min_date = df_merged["date"].min()
df_merged["days_since_start"] = (df_merged["date"] - min_date).dt.days

# Prepare regression inputs
X = df_merged[["days_since_start"]]  # Independent variable
y = df_merged["score"]  # Dependent variable

### Step 5: Train Linear Regression Model ###
model = LinearRegression()
model.fit(X, y)

### Step 6: Predict Inspection Score for 2016-10-10 ###
predict_date = datetime.strptime("2016-10-10", "%Y-%m-%d")
predict_days = (predict_date - min_date).days

predicted_score = model.predict([[predict_days]])[0]

# Print result
print(f"Predicted inspection score for 2016-10-10: {predicted_score:.2f}")
