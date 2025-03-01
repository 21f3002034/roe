import pandas as pd
import glob
import os
import re

# Specify the folder containing your HTML files
html_files = glob.glob("./q1/*.html")

# Create a writer object for Excel output
excel_writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")

for file in html_files:
    # Read all tables from the HTML file
    tables = pd.read_html(file)
    
    for i, table in enumerate(tables):
        # Extract the base file name and sanitize it for Excel sheet names
        raw_name = os.path.basename(file).replace('.html', '')
        
        # Replace invalid characters with an underscore
        sheet_name = re.sub(r'[\\/*?:[\]]', '_', f"{raw_name}_table_{i+1}")
        
        # Truncate the sheet name if necessary (Excel max sheet name length is 31 characters)
        sheet_name = sheet_name[:31]
        
        # Write the table to Excel
        table.to_excel(excel_writer, sheet_name=sheet_name, index=False)

# Save the Excel file
excel_writer.close()
print("Tables successfully converted to Excel!")
