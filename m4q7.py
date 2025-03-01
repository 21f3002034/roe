import os
import sqlite3
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from openai import OpenAI

# OpenAI API key setup (replace 'your-api-key' with your actual key)
client = OpenAI(api_key="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc")

# File paths
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"
db_path = os.path.join(html_folder, "violations.db")

### Step 1: Scrape business_id, latitude, longitude, and description from HTML ###
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
                description = ""

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        for i in range(len(cols) - 1):
                            key = cols[i].text.strip()
                            value = cols[i + 1].text.strip()

                            if key == "business_id":
                                business_id = value
                            elif key == "latitude":
                                try:
                                    latitude = float(value)
                                except ValueError:
                                    latitude = None
                            elif key == "longitude":
                                try:
                                    longitude = float(value)
                                except ValueError:
                                    longitude = None
                            elif key == "description":
                                description = value  # Store description

                # Drop missing values and zero lat/lon
                if business_id and latitude and longitude and (latitude != 0) and (longitude != 0):
                    business_data.append([business_id, latitude, longitude, description])

# Convert to DataFrame
df_business = pd.DataFrame(business_data, columns=["business_id", "latitude", "longitude", "description"])

### Step 2: Extract business_id and description from violations.db ###
conn = sqlite3.connect(db_path)
query = "SELECT business_id, description FROM violations"
df_violations = pd.read_sql_query(query, conn)
conn.close()

# Drop missing values
df_violations.dropna(inplace=True)

# Convert business_id to string for merging
df_business["business_id"] = df_business["business_id"].astype(str)
df_violations["business_id"] = df_violations["business_id"].astype(str)

### Step 3: Merge business and violations data ###
df_merged = pd.merge(df_business, df_violations, on="business_id", suffixes=("_biz", "_vio"))

### Step 4: Filter by latitude and longitude ###
df_filtered = df_merged[
    (df_merged["latitude"] >= 37.7) & (df_merged["latitude"] <= 37.900000000000006) &
    (df_merged["longitude"] >= -122.4) & (df_merged["longitude"] <= -122.2)
]

### Step 5: Compute Embeddings for Descriptions ###
def get_embedding(text):
    """Fetches embedding for the given text using OpenAI API."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(response["data"][0]["embedding"])

df_filtered["embedding"] = df_filtered["description_vio"].apply(get_embedding)

### Step 6: Compute Centroid of Embeddings ###
embedding_matrix = np.stack(df_filtered["embedding"].values)
centroid = np.mean(embedding_matrix, axis=0)

### Step 7: Compute Pythagorean Distance from Centroid ###
df_filtered["distance"] = df_filtered["embedding"].apply(lambda emb: np.linalg.norm(emb - centroid))

### Step 8: Find Most Dissimilar Embeddings (Highest Distance) ###
max_distance = df_filtered["distance"].max()
df_most_dissimilar = df_filtered[df_filtered["distance"] == max_distance]

### Step 9: Count Unique Businesses with Most Dissimilar Embeddings ###
unique_businesses = df_most_dissimilar["business_id"].nunique()

# Print result
print("Number of unique businesses with most dissimilar embeddings:", unique_businesses)
