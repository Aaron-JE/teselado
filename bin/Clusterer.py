# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:07:16 2020

@author: Carlos Moreno Morera & Aarón González
"""
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.fcm import fcm
from infrastructure import boundingbox
import numpy as np
import config as cf
import shapely
import matplotlib.pyplot as plt

class Clusterer:
    
    """
    TO FILL
    
    Attributes
    ----------
    start : int
            TO FILL.
        end : int
            TO FILL.
        
    """
    
    def __init__(self, start=1, end=13): # metric=metrica#):
        """
        Class constructor
        
        Parameters
        ----------
        start : int (optional)
            TO FILL. The default value is 1.
        end : int (optional)
            TO FILL. The default value is 13.
            
        Returns
        -------
        Constructed K_Means class.
        
        """
        self.__start = start
        self.__end = end
    
    def __kmeans(self, points):
        """
        TO FILL.
        
        Parameters
        ----------
        points : TYPE
            DESCRIPTION.
        
        Returns
        -------
        kclusters: TYPE
            DESCRIPTION.
        kcenters: TYPE
            DESCRIPTION.
        
        """

        # Prepare initial centers using K-Means++ method.
        initial_centers = kmeans_plusplus_initializer(points, 10).initialize()
        # Create instance of K-Means algorithm with prepared centers.
        self.__kmeans_instance = kmeans(points, initial_centers)
        # Run cluster analysis and obtain results.
        self.__kmeans_instance.process()
        kclusters = self.__kmeans_instance.get_clusters()
        kcenters = self.__kmeans_instance.get_centers()
        return kclusters, kcenters

    def __cmeans(self, points, nclusters):
        """
        TO FILL

        Parameters
        ----------
        points : TYPE
            DESCRIPTION.
        nclusters : TYPE
            DESCRIPTION.

        Returns
        -------
        clusters : TYPE
            DESCRIPTION.
        centers : TYPE
            DESCRIPTION.
        membership : TYPE
            DESCRIPTION.

        """
        
        # load list of points for cluster analysis
        # initialize
        initial_centers = kmeans_plusplus_initializer(points, nclusters, 
            kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()
        # create instance of Fuzzy C-Means algorithm
        fcm_instance = fcm(points, initial_centers)
        # run cluster analysis and obtain results
        fcm_instance.process()
        clusters = fcm_instance.get_clusters()
        centers = fcm_instance.get_centers()
        membership = fcm_instance.get_membership()
        
        return clusters, centers, membership
    
    def get_clusters(self, points):
        """
        TO FILL

        Parameters
        ----------
        points : TYPE
            DESCRIPTION.

        Returns
        -------
        list
            DESCRIPTION.

        """
        ##self.hull = 
        return [self.__cmeans(points, i) for i in range(self.__start,self.__end)]


    def teselado(self, points):
        """
        TO FILL

        Parameters
        ----------
        points : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #muestrea todo el espacio de la envolvente para conseguir las fronteras 
        #de decision a intervalos regulares 
        #get_hull
        area = boundingbox(points)
        #(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y)
        #sample inside hull
        lat_sample = np.arange(cf.LAT_MIN, cf.LAT_MAX, cf.STEP).tolist()
        lon_sample = np.arange(cf.LON_MIN, cf.LON_MAX, cf.STEP)
        
        _, centers = self.__kmeans(points)
        
        sampling_space = [[x,y] for x in lat_sample for y in lon_sample]
        sampling_space = np.asarray(sampling_space, dtype=np.float32)
        
        prediction = self.__kmeans_instance.predict(sampling_space)
        pol = [[list(sampling_space[index]) for index in 
                [i for i, j in enumerate(prediction) if j == k]] for k in range(centers)]
        hull = [shapely.geometry.MultiPoint(pol[i]).convex_hull.exterior._get_coords() 
                for i in range(len(pol))]
        
        for i in range(len(hull)):
            vertices= []
            vertices[i] = [list(v) for v in  zip(hull[i].xy[0],hull[i].xy[1])]
         
        for i in  range(len(hull)):
            print(i)
            poligonos = []
            vertices = [ list(v) for v in  zip(hull[i].xy[0],hull[i].xy[1])]
            print(vertices)
            poligonos.append(vertices)
            print(poligonos)
        
        plt.plot(hull.xy[1], hull.xy[0])


