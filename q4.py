import pandas as pd
import networkx as nx
from haversine import haversine

# Define the list of connections between cities
connections = '''
New York London
Tokyo Sydney
Paris Berlin
Dubai Mumbai
San Francisco Tokyo
Toronto New York
Shanghai Singapore
Los Angeles Mexico City
Istanbul Athens
Madrid Rome
Bangkok Hong Kong
Seoul Shanghai
Chicago Toronto
Cape Town Nairobi
Melbourne Auckland
Kuala Lumpur Jakarta
Rio de Janeiro Buenos Aires
Berlin Prague
Lima Bogota
Montreal Miami
Santiago Lima
Vancouver San Francisco
Boston Dublin
Oslo Helsinki
Sydney Brisbane
Singapore Bangkok
Zurich Vienna
Tokyo Seoul
Dubai Tel Aviv
Doha Istanbul
Athens Cairo
Lisbon Madrid
Warsaw Budapest
Houston Phoenix
Dallas Atlanta
Stockholm Copenhagen
Hanoi Ho Chi Minh City
Casablanca Algiers
Abu Dhabi Riyadh
Nairobi Accra
Moscow Tbilisi
Addis Ababa Lagos
Tehran Karachi
Lahore Islamabad
Dhaka Colombo
Kathmandu Delhi
Ulaanbaatar Nur-Sultan
Brussels Amsterdam
Perth Jakarta
Tashkent Bishkek
London Paris
Los Angeles San Francisco
Hong Kong Seoul
Chicago Boston
Rome Vienna
Miami Atlanta
Cape Town Addis Ababa
Jakarta Singapore
Mexico City Bogota
Montreal Toronto
Dubai Doha
New York Miami
Tokyo Osaka
Cairo Istanbul
Berlin Warsaw
Rio de Janeiro Lima
Buenos Aires Santiago
Melbourne Sydney
Lisbon Dublin
Helsinki Stockholm
Ho Chi Minh City Bangkok
Casablanca Nairobi
Vienna Prague
Dallas Houston
Phoenix San Diego
Vancouver Seattle
Kuala Lumpur Manila
Manila Taipei
Taipei Hong Kong
Nairobi Accra
Accra Lagos
Addis Ababa Luanda
Luanda Cape Town
Athens Rome
Oslo Brussels
Stockholm Helsinki
Zurich Amsterdam
Tel Aviv Istanbul
Tehran Dubai
Moscow Helsinki
Doha Abu Dhabi
Kuwait City Dubai
Islamabad Delhi
Colombo Mumbai
Karachi Tehran
Yerevan Tbilisi
Tbilisi Baku
Kigali Nairobi
Muscat Dubai
Jeddah Riyadh
Brisbane Perth
Barcelona Paris
Caracas Bogota
Sao Paulo Buenos Aires
Nairobi Addis Ababa
Accra Lagos
Luanda Kinshasa
Wellington Auckland
Perth Wellington
Kigali Nairobi
Mumbai Delhi
Lahore Karachi
Nur-Sultan Almaty
Tashkent Almaty
Ulaanbaatar Beijing
Beijing Shanghai
Shanghai Hong Kong
Hong Kong Tokyo
Tokyo Seoul
Seoul Beijing
Dubai Singapore
Istanbul Bangkok
Cairo Dubai
Istanbul Casablanca
Mumbai Singapore
Dubai Bangkok
'''.strip().split('\n')

# Define city coordinates
city_coords = pd.read_csv('./q4/city_coordinates.csv')
city_coords = city_coords.set_index('City').T.to_dict()

# Create a graph with NetworkX
G = nx.Graph()

# Add edges to the graph with Haversine distance as weight
for conn in connections:
    cities = conn.split()
    if len(cities) != 2:
        print(f"Skipping invalid connection: {conn}")
        continue
    city1, city2 = cities
    if city1 in city_coords and city2 in city_coords:
        coord1 = (city_coords[city1]['Latitude'], city_coords[city1]['Longitude'])
        coord2 = (city_coords[city2]['Latitude'], city_coords[city2]['Longitude'])
        distance = haversine(coord1, coord2)
        G.add_edge(city1, city2, weight=distance)

# Calculate the shortest path
start_city = 'Stockholm'
target_city = 'Toronto'
shortest_path = nx.shortest_path(G, source=start_city, target=target_city, weight='weight')

# Output the result
print(','.join(shortest_path))
