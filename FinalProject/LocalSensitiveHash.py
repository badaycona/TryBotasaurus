"""
Local Sensitive Hashing (LSH) for approximate nearest neighbor search.
This implementation uses a simple hash bucket approach to map high-dimensional data points to lower-dimensional buckets.
"""

import numpy as np
from typing import Optional

class HashBucket:
    def __init__(self, bucket_size, dimension ):
        self.eta = np.random.uniform(0, bucket_size)
        self.dimension = dimension
        self.bucket_size = bucket_size
    def apply(self, x : Optional[np.ndarray]):
        x = (x + self.eta * np.ones(self.dimension)) / self.bucket_size
        x = np.floor(x)
        return hash(x.data.tobytes())
    
        



