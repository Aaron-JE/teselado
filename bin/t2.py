import pandas as pd
import numpy as np
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from config import *
import osmnx as ox
import networkx as nx
import shapely
import matplotlib.pyplot as plt

def query(query_string: str) -> pd.DataFrame:
    """Query."""
    from google.cloud import bigquery
    default_project_id = 'just-data-warehouse'
    client = bigquery.Client(project=default_project_id)
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query_string, job_config=job_config)
    return query_job.result().to_dataframe()

#TODO Mirar como introducir metricas personalizadas en la libreria
def metrica(centroide, punto):
    nodo_centroide = ox.get_nearest_node(G, (centroide))
    nodo_punto =  ox.get_nearest_node(G, (punto))
    return nx.shortest_path_length(G, nodo_centroide, nodo_punto) 


# G = ox.graph_from_bbox(41.471783, 41.357930, 2.014390, 2.305203)
# center_point = [41.405124396565796, 2.180564066230577]
# G = ox.graph_from_point(center_point, 10000)
# graph_map = ox.plot_graph_folium(G, popup_attribute='name', edge_width=2)
# graph_map.save('mapa_grafo.html')

df = query(qrestaurants)
df['restaurant_coordinates'] = list(zip(df.address_latitude, df.address_longitude))              
sample = [list(elem) for elem in  list(df['restaurant_coordinates']) ]

#metric = distance_metric(type_metric.USER_DEFINED, func=metrica)

'''
Standard K-means
'''
def kmeans(points, nclusters):
    # Prepare initial centers using K-Means++ method.
    initial_centers = kmeans_plusplus_initializer(sample, 10).initialize()
    # Create instance of K-Means algorithm with prepared centers.
    kmeans_instance = kmeans(sample, initial_centers)
    # Run cluster analysis and obtain results.
    kmeans_instance.process()
    kclusters = kmeans_instance.get_clusters()
    kcenters = kmeans_instance.get_centers()
    return kclusters, kfinal_centers
# Visualize obtained results
kmeans_visualizer.show_clusters(sample, clusters, final_centers)

'''
C-means
'''
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.fcm import fcm
from pyclustering.utils import read_sample

def cmeans(points, nclusters= 3):
# load list of points for cluster analysis
# initialize
    initial_centers = kmeans_plusplus_initializer(sample, nclusters, kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()
# create instance of Fuzzy C-Means algorithm
    fcm_instance = fcm(sample, initial_centers)
# run cluster analysis and obtain results
    fcm_instance.process()
    clusters = fcm_instance.get_clusters()
    centers = fcm_instance.get_centers()
    membership = fcm_instance.get_membership()
    return clusters, centers, membership

# visualize clustering results
visualizer = cluster_visualizer()
visualizer.append_clusters(clusters, sample)
visualizer.append_cluster(centers, marker='*', markersize=10)
visualizer.show()

#muestrea todo el espacion de la envolvente para conseguir las fronteras de decision a intervalos regulares
lat_sample = np.arange(41.372371, 41.441524, 0.001).tolist()
lon_sample = np.arange(2.104855,2.231566, 0.001)
sampling_space = [[x,y] for x in lat_sample for y in lon_sample]
sampling_space = np.asarray(sampling_space, dtype=np.float32)

prediction = kmeans_instance.predict(sampling_space)

pol = [[sampling_space[index] for index in [i for i, j in enumerate(prediction) if j == k]] for k in range(10)]
points_in_0 = [i for i, j in enumerate(prediction) if j == 0]
points_in_1 = [i for i, j in enumerate(prediction) if j == 1]
pol0 = [sampling_space[index] for index in points_in_0]

#funcion de envolvente convexa


hull = [shapely.geometry.MultiPoint().convex_hull.exterior._get_coords()]

vertices = [list(v) for v in zip(hull.xy[0],hull.xy[1])]


plt.plot(hull.xy[1], hull.xy[0])




