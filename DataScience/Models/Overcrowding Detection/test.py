import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import DBSCAN
import seaborn as sns
import folium
from folium.plugins import HeatMap

def process_data(gps_data):
    # Using DBSCAN to cluster the data
    dbscan = DBSCAN(eps=0.01, min_samples=5)
    clusters = dbscan.fit_predict(gps_data)
    
    df = pd.DataFrame({'Latitude': gps_data[:, 0], 'Longitude': gps_data[:, 1], 'Cluster': clusters})
    num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    colors = cm.rainbow(np.linspace(0, 1, num_clusters))

    plt.figure(figsize=(10, 10))
    for cluster_id, color in zip(set(clusters), colors):
        if cluster_id == -1:
            continue
        cluster_points = df[df['Cluster'] == cluster_id]
        plt.scatter(cluster_points['Longitude'], cluster_points['Latitude'], c=[color], label=f'Cluster {cluster_id}')

    plt.title('Clusters of Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

# Initialize empty arrays for latitudes and longitudes
latitudes = []
longitudes = []

# Define cluster centers
cluster_centers = [ 
    (51.507351, -0.127758),   # London, UK   
]

# Define standard deviation for the distribution of points around the cluster center
std_dev = 0.03

# Number of points per cluster
points_per_cluster = 100

# Generate points for each cluster
for center in cluster_centers:
    lat_center, lon_center = center
    latitudes += list(np.random.normal(lat_center, std_dev, points_per_cluster))
    longitudes += list(np.random.normal(lon_center, std_dev, points_per_cluster))

# Processing the data and plotting
gps_data = np.array([latitudes, longitudes]).T
process_data(gps_data)
# Creating a DataFrame with the latitude and longitude data
heatmap_data = pd.DataFrame({'Latitude': latitudes, 'Longitude': longitudes})

# Plotting the heatmap using Seaborn's kdeplot function
plt.figure(figsize=(10, 10))
sns.kdeplot(x='Longitude', y='Latitude', data=heatmap_data, cmap='Reds', shade=True)
plt.title('Heatmap of Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Calculate the mean latitude and longitude
mean_latitude = np.mean(latitudes)
mean_longitude = np.mean(longitudes)

# Create a base map, centered at the mean coordinates
base_map = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=13)

# Create a list of [lat, lon] pairs for the heatmap
heatmap_data = [[lat, lon] for lat, lon in zip(latitudes, longitudes)]

# Add the heatmap layer to the base map
HeatMap(heatmap_data).add_to(base_map)

# Save the map to an HTML file (optional)
base_map.save('heatmap.html')
