"""
Create a local sensitive function serving quick categorizing datapoints in vicinity with high precision
"""

import numpy as np

class LSHash:
    def __init__(self, bucket_size = 1, dimension = 1):
        self.eta = np.random.uniform(0, bucket_size) * np.ones(dimension)
    def apply(self, vector : np.array):
        
        return None