import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class DBSCANClustering:
    def __init__(self, epsilon, min_samples):
        self.dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)

    def run(self, features, symbols):
        clustering = self.dbscan.fit(features)

        self.plot(features, clustering)

    def plot(self, features, clustering):
        labels = clustering.labels_

        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        # Plot
        unique_labels = set(labels)
        colors = [
            plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))
        ]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = [0, 0, 0, 1]

            class_member_mask = labels == k

            coordinates = features[class_member_mask]
            ax.scatter(
                coordinates[:, 0],
                coordinates[:, 1],
                coordinates[:, 2],
                marker="o",
                color=col,
                alpha=1.0,
                linewidths=1.5,
            )

        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")
        ax.set_zlabel("z axis")

        plt.title(
            "Number of clusters: %d\n Number of noise points: %d "
            % (n_clusters_, n_noise_)
        )
        plt.show()


def optimal_epsilon(features, min_samples):
    # Calculate the average distance between each point
    neighbors = NearestNeighbors(n_neighbors=min_samples)
    neighbors_fit = neighbors.fit(features)
    distances, indices = neighbors_fit.kneighbors(features)

    # Sort distance values in ascending order and plot
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    plt.plot(distances)
    plt.show()


def optimal_min_samples(features):
    # Calculate the min_samples from data dimension
    min_samples = (features.shape[1] * 2) - 1

    return min_samples
