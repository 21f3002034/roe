# extract each column and its value from html tables
import os
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import subprocess
import json
from typing import Dict, Any, List

# Path to dataset
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(html_folder, "violations.db")

# Step 1: Extract business_id for postal code 94110 from HTML files
business_ids = []

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
                latitude = None
                longitude = None

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        for i in range(len(cols) - 1):
                            if cols[i].text.strip() == "business_id":
                                business_id = cols[i + 1].text.strip()
                            if cols[i].text.strip() == "postal_code":
                                postal_code = cols[i + 1].text.strip()
                            if cols[i].text.strip() == "latitude":
                                latitude = cols[i + 1].text.strip()
                            if cols[i].text.strip() == "longitude":
                                longitude = cols[i + 1].text.strip()
                            if business_id and postal_code and latitude != "null" and latitude is not None and longitude != "null" and longitude is not None:
                                business_ids.append([business_id, postal_code, float(latitude), float(longitude)]) 

#print(business_ids[0])

import os
import pdfplumber
import sqlite3
import pandas as pd
from datetime import datetime

inspection_data = []
pdf_folder =  r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
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
                            score = row[2].strip()  # Third column: score
                            type_table = row[3].strip()  # Fourth column: type

                            # Convert to datetime for proper comparison
                            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                            # Only keep records on or after the cutoff date
                            if score.isdigit():
                                inspection_data.append([business_id, date_str, score, type_table])

                        except (IndexError, AttributeError, ValueError):
                            continue  # Skip invalid rows

#print(inspection_data[0])

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = """
    SELECT business_id, description
    FROM violations
"""

df_violations = pd.read_sql_query(query, conn)
conn.close()

print(df_violations.head())
df_business = pd.DataFrame(business_ids, columns=['business_id', 'postal_code', 'latitude', 'longitude'])
df_violations = df_violations.astype(str)
df=pd.merge(df_business,df_violations, on='business_id', how='inner')
#print(df.head())

df_filtered = df[(df['latitude'] >= 37.7) & (df['latitude'] <= 37.900000000000006)]
df_filtered = df_filtered[(df_filtered['longitude'] >= -122.2) & (df_filtered['longitude'] <= -122.4)]  
#print(df_filtered.head())





# def query_gpt(user_input: str) -> Dict[str, Any]:
#     url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions" 
# url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"                   
#     AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc"

import requests
import pandas as pd
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc"
# Your API URL and token
url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions" 


# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AIPROXY_TOKEN}"
}


# Function to get embeddings
def get_embedding(text):
    print(f"Getting embedding for: {text}")
    data = {
        "model": "text-embedding-3-small",
        "input": text
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()["data"][0]["embedding"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Apply embedding function to descriptions
df_filtered["embedding"] = df_filtered["description"].apply(lambda x: print(f"Processing: {x}") or get_embedding(x))

# Print the DataFrame with embeddings
print(df_filtered)
