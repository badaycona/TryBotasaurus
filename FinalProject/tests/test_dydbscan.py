# filepath: c:\Users\Admin\Downloads\Code\FinalProject\tests\test_dydbscan.py
import unittest
import numpy as np
from DyDBSCAN import DynamicDBSCAN

class TestDynamicDBSCAN(unittest.TestCase):
    def test_add_point(self):
        data = np.random.randint(0, 10, (100, 4))
        dbscan = DynamicDBSCAN(minP=3, t=2, eps=1.5, initial_data=data)
        idx = dbscan.add_point(np.array([1, 2, 3, 4]))
        self.assertIn(idx, dbscan.core_points.union(dbscan.non_core_points))
        print(dbscan.core_points)
        print(dbscan.non_core_points)
if __name__ == '__main__':
    unittest.main()