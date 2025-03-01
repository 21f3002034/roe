import os
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

# File path to the folder containing HTML files
html_folder = r"G:\001 IITM DATASCIENCE\002 Diploma\TDS\roe\mock\mock_roe_4"

# Step 1: Extract postal_code, latitude, and longitude from HTML files
restaurant_data = []

for filename in os.listdir(html_folder):
    if filename.startswith("biz-") and filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            for table in soup.find_all("table"):
                rows = table.find_all("tr")

                postal_code = None
                latitude = None
                longitude = None

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        for i in range(len(cols) - 1):
                            key = cols[i].text.strip()
                            value = cols[i + 1].text.strip()

                            if key == "postal_code":
                                postal_code = value
                            elif key == "latitude" and value.lower() != "null":
                                try:
                                    latitude = round(float(value), 6)  # Keep precision for accuracy
                                except ValueError:
                                    latitude = None
                            elif key == "longitude" and value.lower() != "null":
                                try:
                                    longitude = round(float(value), 6)
                                except ValueError:
                                    longitude = None

                # Drop rows with missing values
                if postal_code and latitude is not None and longitude is not None:
                    restaurant_data.append([postal_code, latitude, longitude])

# Convert to DataFrame
df_restaurants = pd.DataFrame(restaurant_data, columns=["postal_code", "latitude", "longitude"])
# Convert to DataFrame

# Drop rows where postal_code is null or invalid
df_restaurants = df_restaurants[df_restaurants["postal_code"].notnull()]
df_restaurants = df_restaurants[df_restaurants["postal_code"].str.lower() != "null"]
# Step 2: Compute centroid for each postal code
df_centroids = df_restaurants.groupby("postal_code", as_index=False).agg({
    "latitude": "mean",
    "longitude": "mean"
}).rename(columns={"latitude": "centroid_lat", "longitude": "centroid_lon"})

# Merge centroids with restaurant data
df_merged = df_restaurants.merge(df_centroids, on="postal_code")

# Step 3: Compute Pythagorean distance from each restaurant to its centroid
df_merged["distance"] = np.sqrt((df_merged["latitude"] - df_merged["centroid_lat"])**2 + 
                                (df_merged["longitude"] - df_merged["centroid_lon"])**2)

# Step 4: Compute average distance per postal code
df_avg_distance = df_merged.groupby("postal_code", as_index=False)["distance"].mean().rename(
    columns={"distance": "average_distance_from_centroid"}
)

# Step 5: Find the postal code with the highest average distance
max_distance_postal_code = df_avg_distance.loc[df_avg_distance["average_distance_from_centroid"].idxmax()]

# Print results
print("\nPostal Code with the Highest Average Distance from Centroid:")
print(max_distance_postal_code)
