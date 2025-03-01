import os
import pdfplumber
from bs4 import BeautifulSoup
import pandas as pd

# File Paths
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
pdf_path = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4\inspections-2014-05.pdf"  # Ensure correct file name

### 1. Extract business_id, latitude, and longitude from HTML ###
business_data = []

for filename in os.listdir(html_folder):
    if filename.startswith("biz-") and filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            for table in soup.find_all("table"):
                rows = table.find_all("tr")

                business_id = None
                latitude = None
                longitude = None

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        
                        for i in range(len(cols) - 1):
                            key = cols[i].text.strip()
                            value = cols[i + 1].text.strip()
                            
                            if key == "business_id":
                                business_id = value
                            elif key == "latitude" and value.lower() != "null":
                                try:
                                    latitude = float(value)
                                except ValueError:
                                    latitude = None
                            elif key == "longitude" and value.lower() != "null":
                                try:
                                    longitude = float(value)
                                    longitude = float(value)
                                except ValueError:
                                    longitude = None

                # Only keep businesses with valid lat & long
                if business_id and latitude is not None and longitude is not None:
                    business_data.append([business_id, latitude, longitude])
#print(business_data)

# Convert to DataFrame
df_business = pd.DataFrame(business_data, columns=["business_id", "latitude", "longitude"])
print(df_business)
### 2. Extract business_id and score from PDF ###
inspection_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        #print(table)
        if table:
            for row in table[1:]:  # Skip header
                
                try:
                    business_id = row[0].strip()
                    score = row[2].strip()
                    
                    # Only keep valid numeric scores
                    #score = int(score) if score.isdigit() else 0  
                    if business_id and score.isdigit():
                        inspection_data.append([business_id, int(score)])   
                except (IndexError, AttributeError):
                    continue  # Skip invalid rows

# Convert to DataFrame
df_inspections = pd.DataFrame(inspection_data, columns=["business_id", "score"])

### 3. Join both datasets on business_id ###
df_merged = pd.merge(df_business, df_inspections, on="business_id")
df_merged["latitude"] = df_merged["latitude"].round(2)
df_merged["longitude"] = df_merged["longitude"].round(2)

# Compute average score per (latitude, longitude)


### 4. Compute average score per (latitude, longitude) ###
df_avg_score = df_merged.groupby(["latitude", "longitude"], as_index=False).agg({"score": "mean"})
df_avg_score.to_csv("average_scores_by_location.csv", index=False)
### 5. Find the highest average score ###
max_avg_score = df_avg_score["score"].max()
#print(max_avg_score)
### 6. Print result ###
print("Highest average inspection score in May 2015:", round(max_avg_score, 2))
