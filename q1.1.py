from bs4 import BeautifulSoup

gold_sum = 0

# Loop through HTML files named file1.html to file10.html
for i in range(1, 11):
    with open(f"q1//file{i}.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
        # Find all tables in the HTML file
        tables = soup.find_all("table")
        
        for table in tables:
            rows = table.select("tbody > tr")
            
            for r in rows:
                col_data = r.find_all("td")
                
                # Extract and clean data from columns
                ticket_type = col_data[0].string.upper().strip()
                
                if ticket_type == "GOLD":
                    units = int(col_data[1].string.strip())
                    price = round(float(col_data[2].string.strip()), 2)
                    
                    # Calculate total for Gold items
                    total = round(units * price, 2)
                    gold_sum += total

print(round(gold_sum, 2))
