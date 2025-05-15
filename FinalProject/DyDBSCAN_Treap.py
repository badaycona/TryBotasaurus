import numpy as np
import random
from typing import Optional, List, Dict, Set
from collections import defaultdict
import time
from hash import LSHash
from TreapImp import EulerTourForest
from pprint import pprint

class DynamicDBSCAN():
    __slots__ = ('minP', 't', 'eps', 'data', 'core_points',
                  'non_core_points', 'forest', 'hash_functions', 'hash_buckets')

    def __init__(self, minP: int, t: int, eps: float, initial_data: Optional[np.ndarray] = None):
        self.minP = minP
        self.eps = eps
        self.t = t         # Number of hash functions

        dim=initial_data.shape[1] if initial_data is not None else 0

        #Storing the dataset as a dictionary from indices to vectors
        self.data : Dict[int, np.ndarray] = {}

        
        self.core_points : Set[int] = set()
        self.non_core_points : Set[int] = set()

        self.forest = EulerTourForest()

        # Initialise the hash functions. For each has function, we maintain a dictionary of hash buckets.
        self.hash_functions: List[LSHash] = [LSHash(2 * self.eps, dim) for _ in range(self.t)]
        self.hash_buckets : List[Dict[int, List[int]]]= [{} for _ in range(self.t)]

        if initial_data is not None:
            self._initialize_data(initial_data)
            self._identify_core_points()
            self._link_all_points()
        
    def _initialize_data(self, initial_data: np.ndarray):

        for i in range(initial_data.shape[0]):
            point = initial_data[i]

            # Add this point in the dynamic forest           
            index = self.forest.add()

            self.data[index] = point
            self.non_core_points.add(index)
            self._insert_to_buckets(point, index)

    def _insert_to_buckets(self, point: np.ndarray, index: int):
        # For each hash function, we compute the hash value of the point and add it to the corresponding bucket
        for i , hash_fn in enumerate(self.hash_functions):
            hash_val=hash_fn.apply(point)
            self.hash_buckets[i].setdefault(hash_val, []).append(index)
    def _identify_core_points(self):
        # Find the core points
        for j in range(self.t):
            for bucket in self.hash_buckets[j].values():
                if len(bucket) >= self.minP:
                    self.core_points.update(bucket)
                    self.non_core_points.difference_update(set(bucket))
    def _link_all_points(self):
        for i in self.core_points:   
            self.link_core_point(i)

        for i in self.non_core_points:        
            self.link_non_core_point(i)

    def link_core_point(self, point_index: int, new_point=False):
        candidates_to_check: Set[int] = set() 
        for j in range(self.t):
            this_hash_value = self.hash_functions[j].apply(self.data[point_index])
            bucket = self.hash_buckets[j][this_hash_value]

            if new_point:
                # If this is a new point, we will link it to the first core point in the bucket
                for i in reversed(bucket):
                    if i in self.core_points and i != point_index:
                        self.forest.link(point_index, i)
                        break
                    else:
                        candidates_to_check.add(i)
            else:
                # We will link point_index to the point with the largest index not more than its own
                # In this way, the graph on the core points in the bucket will always be a path
                pre, _next=None, None
                for i in bucket:
                    if i not in self.core_points:
                        candidates_to_check.add(i)
                        continue
                    if i < point_index:
                        if pre is None or pre < i:
                            pre = i
                    if i > point_index:
                        if _next is None or _next > i:
                            _next = i

                # If the previous point and next point are connected in the forest, disconnect them
                must_link_both = False
                if (_next is not None and pre is not None and
                        _next in self.forest.nodes[pre].neighbors):
                    
                    self.forest.cut(pre, _next)
                    must_link_both = True

                if must_link_both or pre is not None:
                    self.forest.link(point_index, pre)
                if must_link_both:
                    self.forest.link(point_index, _next)

        # Update non-core points
        for i in candidates_to_check:
            self.link_non_core_point(i)

    def link_non_core_point(self, point_index: int):
        if len(self.forest.nodes[point_index].neighbors) > 0:
            return

        for i, hash_fn in enumerate(self.hash_functions):
            hash_val=hash_fn.apply(self.data[point_index])
            bucket=self.hash_buckets[i][hash_val]
            for j in bucket:
                if j in self.core_points:
                    self.forest.link(point_index, j)
                    return

    def unlink_non_core_point(self, point_index: int): 
        if len(self.forest.nodes[point_index].neighbors) > 0:
            list(self.forest.nodes[point_index].neighbors)
            for point in list(self.forest.nodes[point_index].neighbors):
                self.forest.cut(point, point_index)

    def add_point(self, point: np.ndarray) -> int:
        # Add this point as a disconnected point in the dynamic forest
        
        index = self.forest.add()
        self.data[index] = point

        # Get the set of new core points
        new_core_points : Set[int]= set()
        for j in range(self.t):
            this_hash_value = self.hash_functions[j].apply(point)
            if this_hash_value not in self.hash_buckets[j]:
                self.hash_buckets[j][this_hash_value] = [index]
            else:
                self.hash_buckets[j][this_hash_value].append(index)

            # Check whether the new point is a core point
            if len(self.hash_buckets[j][this_hash_value]) > self.minP:
                new_core_points.add(index)
            if len(self.hash_buckets[j][this_hash_value]) == self.minP:
                new_core_points.update(self.hash_buckets[j][this_hash_value])

        new_core_points = new_core_points.difference(self.core_points)
        self.core_points.update(new_core_points)
        self.non_core_points.difference_update(new_core_points)

        # If the new point is not a core point, we just process it like any non-core point
        if not new_core_points:
            self.non_core_points.add(index)
            self.link_non_core_point(index)
        else:

            for new_core_point in new_core_points:
                self.unlink_non_core_point(new_core_point)
                self.link_core_point(new_core_point, new_point=(len(new_core_points) == 1))

        return index


    def get_cluster(self, index: int):
        return self.forest.root(index) if self.forest.nodes[index].neighbors else -1
if __name__=='__main__':
    for i in range(40):
        data=np.array([np.random.randint(0, 10, (1, 4)) for _ in range(360)])
        minP=3
        t=2
        eps=1.5

        dbscan=DynamicDBSCAN(minP, t, eps, data)

        dbscan.add_point(np.array([1, 2, 3, 4]))
        
        
        print('Core points:')
        print(dbscan.core_points)

        print('Non-core points:')
        print(dbscan.non_core_points)

    
    