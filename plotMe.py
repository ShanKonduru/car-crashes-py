import geopandas as gpd
import folium
from folium import plugins
import pandas as pd

# Replace 'your_file.csv' with the actual name of your CSV file
csv_file = 'MyUSAVisit.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Download the US states shapefile from Natural Earth Data
# You can find the shapefile at: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-1-states-provinces/
us_states = gpd.read_file('ne_110m_admin_1_states_provinces.shp')

# Print information about the CSV DataFrame
print("CSV DataFrame Information:")
print(df.info())

# Print the first few rows of the CSV DataFrame
print("First few rows of the CSV DataFrame:")
print(df.head())

# Print information about the US states GeoDataFrame
print("US States GeoDataFrame Information:")
print(us_states.info())

# Print the first few rows of the US states GeoDataFrame
print("First few rows of the US States GeoDataFrame:")
print(us_states.head())

# Merge the US states GeoDataFrame with your data based on the 'state_abbr' column
merged_data = us_states.merge(df, how='left', left_on='state_abbr', right_on='state_abbr')

# Print information about the merged dataset
print("Merged Dataset Information:")
print(merged_data.info())

# Convert 'Days_stayed' column to numeric if it's not already
merged_data['Days_stayed'] = pd.to_numeric(merged_data['Days_stayed'], errors='coerce')

# Print the first few rows of the merged dataset
print("First few rows of the Merged Dataset:")
print(merged_data.head())

# Create a Folium map centered around the USA
m = folium.Map(location=[37, -95], zoom_start=4)

# Add a Marker Cluster to the map for better visualization of multiple points
marker_cluster = plugins.MarkerCluster().add_to(m)

# Iterate over each row in the merged data and add markers
for index, row in merged_data.iterrows():
    state_abbr = row['state_abbr']
    days_stayed = row['Days_stayed'] if not pd.isnull(row['Days_stayed']) else 0
    tooltip = f"State: {state_abbr}\nTotal Days Stayed: {days_stayed}"

    # Add markers to the Marker Cluster
    folium.Marker([row['geometry'].centroid.y, row['geometry'].centroid.x],
                  popup=tooltip).add_to(marker_cluster)

# Save the map as an HTML file
m.save('visited_places_map.html')
