import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


class ApplicabilityDomain:

    def __init__(self):

        self.scaler = StandardScaler()
        self.pca = PCA(random_state=46)

    def _preprocess_data(self, train_data, test_data, n_components=None):

        train_data_scaled = self.scaler.fit_transform(train_data)
        test_data_scaled = self.scaler.transform(test_data)

        if n_components is None:
            self.pca = PCA(n_components=train_data.shape[1], random_state=46)
        else:
            self.pca = PCA(n_components=n_components, random_state=46)
        
        self.pca.fit(train_data_scaled)
        n_components_needed = np.argmax(np.cumsum(self.pca.explained_variance_ratio_) >= 0.8) + 1
        self.pca = PCA(n_components=n_components_needed)
        self.pca.fit(train_data_scaled)

        train_scores = self.pca.transform(train_data_scaled)
        test_scores = self.pca.transform(test_data_scaled)

        return train_scores, test_scores

    def distance_to_model(self, train_data, test_data, n_components=None):

        train_scores, test_scores = self._preprocess_data(train_data, test_data, n_components)
        
        train_reconstructed = self.pca.inverse_transform(train_scores)
        test_reconstructed = self.pca.inverse_transform(test_scores)
        
        test_residuals = test_data - test_reconstructed
        dmodx = np.sqrt(np.sum(test_residuals**2, axis=1))

        mean_dmodx = np.mean(dmodx)
        std_dmodx = np.std(dmodx)
        threshold = mean_dmodx + 3 * std_dmodx
        
        return dmodx > threshold

    def distance_to_centroid(self, train_data, test_data, n_components=None):

        train_scores, test_scores = self._preprocess_data(train_data, test_data, n_components)

        centroid = np.mean(train_scores, axis=0)
        distances_test = np.linalg.norm(test_scores - centroid, axis=1)
        
        mean_distance = np.mean(np.linalg.norm(train_scores - centroid, axis=1))
        std_distance = np.std(np.linalg.norm(train_scores - centroid, axis=1))
        threshold = mean_distance + 3 * std_distance
        
        return distances_test > threshold

    def distance_to_nearest_neighbors(self, train_data, test_data, n_components=None):

        train_scores, test_scores = self._preprocess_data(train_data, test_data, n_components)

        nbrs = NearestNeighbors(n_neighbors=6).fit(train_scores)
        distances_train, _ = nbrs.kneighbors(train_scores)
        distances_train = distances_train[:, 1:]

        mean_distances_train = np.mean(distances_train, axis=1)
        mean_distance = np.mean(mean_distances_train)
        std_distance = np.std(mean_distances_train)
        threshold = mean_distance + 3 * std_distance

        distances_test, _ = nbrs.kneighbors(test_scores)
        distances_test = distances_test[:, 1:]
        mean_distances_test = np.mean(distances_test, axis=1)

        return mean_distances_test > threshold

    def majority_vote_outliers(self, train_data, y_train, test_data, n_components=None):

        train_scores, test_scores = self._preprocess_data(train_data, test_data, n_components)

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(train_scores, y_train)
        neighbors = knn.kneighbors(test_scores, return_distance=False)

        outliers = []
        for neighbor_indices in neighbors:
            neighbor_outputs = y_train[neighbor_indices]
            majority_vote = np.bincount(neighbor_outputs).argmax()
            if np.sum(neighbor_outputs == majority_vote) >= 3:
                outliers.append(False)
            else:
                outliers.append(True)

        return np.array(outliers)

    def single_vote_outliers(self, train_data, y_train, test_data, n_components=None):
        
        train_scores, test_scores = self._preprocess_data(train_data, test_data, n_components)

        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(train_scores, y_train)
        neighbors = knn.kneighbors(test_scores, return_distance=False)

        outliers = []
        for neighbor_indices in neighbors:
            neighbor_outputs = y_train[neighbor_indices]
            majority_vote = np.bincount(neighbor_outputs).argmax()
            if np.sum(neighbor_outputs == majority_vote) == 1:
                outliers.append(False)
            else:
                outliers.append(True)

        return np.array(outliers)

    def ensemble_outliers(self, train_data, y_train, test_data):

        results = []
        for method in [self.distance_to_model, self.distance_to_centroid, 
                       self.distance_to_nearest_neighbors, self.majority_vote_outliers,
                       self.single_vote_outliers]:
            if method in [self.distance_to_model, self.distance_to_centroid, self.distance_to_nearest_neighbors]:
                outliers = method(train_data, test_data)
            else:
                outliers = method(train_data, y_train, test_data)
            results.append(outliers)

        n_false_outliers = np.sum(~np.array(results), axis=0)

        ensemble_outliers = n_false_outliers < 3

        return ensemble_outliers