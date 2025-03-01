import pandas as pd
import glob

# Specify the folder containing the HTML files
html_files = glob.glob("./q1/*.html")

total_sales = 0.0

for file in html_files:
    # Read all tables from the HTML file
    tables = pd.read_html(file)
    
    for table in tables:
        # Check if the table has the expected columns
        if {'Type', 'Units', 'Price'}.issubset(table.columns):
            
            # Filter rows where Type is 'Gold'
            gold_items = table[table['Type'].str.lower() == 'gold']
            
            # Calculate total sales for 'Gold' items
            # Ensure 'Units' and 'Price' are numeric
            gold_items['Units'] = pd.to_numeric(gold_items['Units'], errors='coerce')
            gold_items['Price'] = pd.to_numeric(gold_items['Price'], errors='coerce')
            
            # Compute sales and add to the total
            total_sales += (gold_items['Units'] * gold_items['Price']).sum()

# Round the total sales to 2 decimal places
total_sales = round(total_sales, 2)

print(f"Total sales for 'Gold' ticket type: {total_sales}")

