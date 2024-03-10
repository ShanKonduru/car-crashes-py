import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load your dataset into a Pandas DataFrame
df = pd.read_csv('car_crashes.csv')

# Print the first few rows of your dataset
print("First few rows of your dataset:")
print(df.head())

# Create GeoDataFrame with U.S. state geometries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter to include only the USA
us_states = world[world['iso_a3'] == 'USA']
# Print the first few rows of the GeoDataFrame
print("\nFirst few rows of the GeoDataFrame:")
print(us_states.head())

# Set the index to 'abbrev' for both DataFrames
df.set_index('abbrev', inplace=True)
us_states.set_index('iso_a3', inplace=True)

# Print the first few rows of the GeoDataFrame
print("\nFirst few rows of the GeoDataFrame:")
print(us_states.head())

# Join the GeoDataFrame with the DataFrame based on the index
gdf = us_states.join(df)

# Reset the index
gdf.reset_index(inplace=True)

# Print the first few rows of the resulting GeoDataFrame
print("\nFirst few rows of the resulting GeoDataFrame:")
print(gdf.head())

# Create an interactive map using Folium
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=3)

# Add a Marker Cluster to the map for better visualization of multiple points
marker_cluster = MarkerCluster().add_to(m)

# Add markers for each state
for index, row in gdf.iterrows():
    state_name = row['name']
    total_crashes = row['total'] if not pd.isnull(row['total']) else 0
    folium.Marker([row['geometry'].centroid.y, row['geometry'].centroid.x], 
                  popup=f"State: {state_name}\nTotal Crashes: {total_crashes}").add_to(marker_cluster)

# Display the map
m.save('geospatial_dashboard.html')
