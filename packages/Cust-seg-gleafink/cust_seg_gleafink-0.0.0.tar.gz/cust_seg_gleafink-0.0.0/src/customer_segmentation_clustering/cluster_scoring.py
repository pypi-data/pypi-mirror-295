# cluster_scoring.py

import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min

class ClusterScoring:
    def __init__(self, df: pd.DataFrame, labels: pd.Series):
        self.df = df
        self.labels = labels

    def cluster_summary(self):
        """
        Compute cluster summary statistics: average, range, and count of each feature within clusters.

        Returns:
        - dict: Dictionary with cluster labels as keys and summary statistics as values
        """
        summary = {}
        for label in np.unique(self.labels):
            cluster_data = self.df[self.labels == label]
            summary[label] = {
                'Average': cluster_data.mean().to_dict(),
                'Range': {col: (cluster_data[col].min(), cluster_data[col].max()) for col in cluster_data.columns},
                'Count': len(cluster_data)
            }
        return summary

    def points_within_sigma(self, centroids: pd.DataFrame, sigma: float = 1.0):
        """
        Compute the number of data points within one sigma-limit from the centroid for each cluster.

        Parameters:
        - centroids (pd.DataFrame): DataFrame with cluster centroids
        - sigma (float): Sigma limit

        Returns:
        - dict: Dictionary with cluster labels as keys and count of points within sigma limit as values
        """
        points_within_sigma = {}
        for label in centroids.index:
            centroid = centroids.loc[label].values
            distances = np.linalg.norm(self.df[self.labels == label] - centroid, axis=1)
            std_dev = np.std(distances)
            points_within_sigma[label] = np.sum(distances <= sigma * std_dev)
        return points_within_sigma

    def avg_intra_cluster_distance(self, centroids: pd.DataFrame):
        """
        Compute the average distance of all the points from the centroid for each cluster.

        Parameters:
        - centroids (pd.DataFrame): DataFrame with cluster centroids

        Returns:
        - dict: Dictionary with cluster labels as keys and average intra-cluster distance as values
        """
        avg_distances = {}
        for label in centroids.index:
            centroid = centroids.loc[label].values
            distances = np.linalg.norm(self.df[self.labels == label] - centroid, axis=1)
            avg_distances[label] = np.mean(distances)
        return avg_distances

    def points_from_other_clusters(self, centroids: pd.DataFrame, sigma: float = 1.0):
        """
        Compute the number of data points from other clusters within 1 sigma and 2 sigma distances.

        Parameters:
        - centroids (pd.DataFrame): DataFrame with cluster centroids
        - sigma (float): Sigma limit

        Returns:
        - dict: Dictionary with cluster labels as keys and counts of points from other clusters within sigma limits as values
        """
        points_within_sigma = {}
        for label in centroids.index:
            centroid = centroids.loc[label].values
            distances = np.linalg.norm(self.df[self.labels != label] - centroid, axis=1)
            std_dev = np.std(distances)
            points_within_sigma[label] = {
                'Within 1 Sigma': np.sum(distances <= sigma * std_dev),
                'Within 2 Sigma': np.sum(distances <= 2 * sigma * std_dev)
            }
        return points_within_sigma

    def compute_centroids(self) -> pd.DataFrame:
        """
        Compute the centroids for each cluster.

        Returns:
        - pd.DataFrame: DataFrame with cluster centroids
        """
        centroids = self.df.groupby(self.labels).mean()
        return centroids

    def score_clusters(self):
        """
        Score and visualize cluster behavior.

        Returns:
        - dict: Dictionary with various cluster scores and summaries
        """
        centroids = self.compute_centroids()
        summary = self.cluster_summary()
        points_within_sigma = self.points_within_sigma(centroids)
        avg_distances = self.avg_intra_cluster_distance(centroids)
        points_from_other_clusters = self.points_from_other_clusters(centroids)

        return {
            'Summary': summary,
            'Points Within Sigma': points_within_sigma,
            'Average Intra-Cluster Distance': avg_distances,
            'Points From Other Clusters': points_from_other_clusters
        }
