from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from typing import List
import numpy as np

class ClusteringEvaluator:
   

    def __init__(self, ground_truth: List[int]):
       
        self.ground_truth = np.array(ground_truth)

    def evaluate(self, predicted_labels: List[int]) -> dict:
       
        predicted_labels = np.array(predicted_labels)

        nmi = normalized_mutual_info_score(self.ground_truth, predicted_labels)
        ari = adjusted_rand_score(self.ground_truth, predicted_labels)

        return {
            "NMI": round(nmi, 4),
            "ARI": round(ari, 4)
        }