import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score
class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_ = None

    def fit(self, X):
        n = len(X)
        self.labels_ = [-1] * n  # -1 = noise
        cluster_id = 0
        visited = [False] * n

        def region_query(p_idx):
            neighbors = []
            for q_idx in range(n):
                if np.linalg.norm(X[p_idx] - X[q_idx]) <= self.eps:
                    neighbors.append(q_idx)
            return neighbors

        def expand_cluster(p_idx, neighbors, cluster_id):
            self.labels_[p_idx] = cluster_id
            i = 0
            while i < len(neighbors):
                q_idx = neighbors[i]
                if not visited[q_idx]:
                    visited[q_idx] = True
                    q_neighbors = region_query(q_idx)
                    if len(q_neighbors) >= self.min_samples:
                        neighbors += [n for n in q_neighbors if n not in neighbors]
                if self.labels_[q_idx] == -1:
                    self.labels_[q_idx] = cluster_id
                i += 1

        for i in range(n):
            if visited[i]:
                continue
            visited[i] = True
            neighbors = region_query(i)
            if len(neighbors) < self.min_samples:
                self.labels_[i] = -1  # noise
            else:
                cluster_id += 1
                expand_cluster(i, neighbors, cluster_id)

        return self

if __name__ == "__main__":
    from sklearn.datasets import make_moons
    import matplotlib.pyplot as plt

    X, _ = make_moons(n_samples=300, noise=0.1)

    db = DBSCAN(eps=0.2, min_samples=5)
    db.fit(X)
    labels = db.labels_

    print('ARI:', adjusted_rand_score(_, labels))   

    
