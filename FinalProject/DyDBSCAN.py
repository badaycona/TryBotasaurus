import numpy as np
# import random # random không còn được dùng trực tiếp ở đây nữa
from typing import Optional, List, Dict, Set
# from collections import defaultdict # không cần thiết nữa
# import time # không cần thiết nữa
from hash import LSHash # Giả sử file hash.py tồn tại và đúng
from ETTImplementation2 import EulerTourForest # Giả sử file ETTImplementation2.py tồn tại và đúng
# from pprint import pprint # không cần thiết nữa
from BST import BinarySearchTree # Import BST của bạn

class DynamicDBSCAN():
    __slots__ = ('minP', 't', 'eps', 'data', 'core_points',
                  'non_core_points', 'forest', 'hash_functions', 
                  'hash_bucket_lists', 'hash_bucket_bsts') # Thay đổi hash_buckets

    def __init__(self, minP: int, t: int, eps: float, initial_data: Optional[np.ndarray] = None):
        self.minP = minP
        self.eps = eps
        self.t = t

        dim = initial_data.shape[1] if initial_data is not None and initial_data.ndim == 2 else 0
        if initial_data is not None and initial_data.ndim == 1: # Xử lý trường hợp 1 điểm dữ liệu ban đầu
            dim = initial_data.shape[0]


        self.data: Dict[int, np.ndarray] = {}
        self.core_points: Set[int] = set()
        self.non_core_points: Set[int] = set()
        self.forest = EulerTourForest()

        self.hash_functions: List[LSHash] = [LSHash(2 * self.eps, dim) for _ in range(self.t)]
        # Lưu trữ 2 dạng bucket:
        # 1. Danh sách tất cả các điểm trong bucket (để tìm non-core và khi new_point=True)
        self.hash_bucket_lists: List[Dict[int, List[int]]] = [{} for _ in range(self.t)]
        # 2. BST chứa các core_points trong bucket (để tìm pre/next nhanh)
        self.hash_bucket_bsts: List[Dict[int, BinarySearchTree]] = [{} for _ in range(self.t)]


        if initial_data is not None:
            self._initialize_data(initial_data)
            self._identify_and_build_bsts_for_core_points() # Đổi tên hàm
            self._link_all_points()

    def _initialize_data(self, initial_data: np.ndarray):
        # Xử lý trường hợp initial_data chỉ có 1 điểm
        if initial_data.ndim == 1:
            initial_data = initial_data.reshape(1, -1)

        for i in range(initial_data.shape[0]):
            point = initial_data[i]
            index = self.forest.add()
            self.data[index] = point
            self.non_core_points.add(index) # Ban đầu tất cả là non-core
            self._insert_to_bucket_lists(point, index)

    def _insert_to_bucket_lists(self, point: np.ndarray, index: int):
        for i, hash_fn in enumerate(self.hash_functions):
            hash_val = hash_fn.apply(point)
            self.hash_bucket_lists[i].setdefault(hash_val, []).append(index)

    def _remove_from_bucket_bsts(self, point_index: int):
        """Loại bỏ một điểm khỏi tất cả các BST mà nó có thể thuộc về."""
        point_data = self.data.get(point_index)
        if point_data is None:
            return
        for i, hash_fn in enumerate(self.hash_functions):
            hash_val = hash_fn.apply(point_data)
            if hash_val in self.hash_bucket_bsts[i]:
                self.hash_bucket_bsts[i][hash_val].delete(point_index)


    def _identify_and_build_bsts_for_core_points(self):
        # self.core_points.clear() # Xóa để xác định lại từ đầu
        # self.non_core_points = set(self.data.keys()) # Reset non-core

        potential_new_core_points = set()
        for j in range(self.t):
            for hash_val, bucket_list in self.hash_bucket_lists[j].items():
                if len(bucket_list) >= self.minP:
                    # Tất cả các điểm trong bucket này là core points tiềm năng
                    for point_idx_in_bucket in bucket_list:
                        potential_new_core_points.add(point_idx_in_bucket)
        
        # Cập nhật core_points và non_core_points sets
        newly_identified_core = potential_new_core_points - self.core_points
        lost_core_status = self.core_points - potential_new_core_points # Nếu có logic xóa điểm

        self.core_points.update(newly_identified_core)
        self.non_core_points.difference_update(newly_identified_core)
        
        # Xử lý những điểm mất tư cách core (nếu cần)
        for pt_idx in lost_core_status:
            self._remove_from_bucket_bsts(pt_idx) # Xóa khỏi BST
            self.non_core_points.add(pt_idx)
            self.unlink_non_core_point(pt_idx) # Unlink
            # Sau đó có thể cần link lại như non-core
            self.link_non_core_point(pt_idx)

        # Xây dựng/Cập nhật BSTs cho các core points mới
        for j in range(self.t):
            for hash_val, bucket_list in self.hash_bucket_lists[j].items():
                if hash_val not in self.hash_bucket_bsts[j]:
                    self.hash_bucket_bsts[j][hash_val] = BinarySearchTree()
                
                current_bst = self.hash_bucket_bsts[j][hash_val]
                for point_idx_in_bucket in bucket_list:
                    if point_idx_in_bucket in self.core_points:
                        current_bst.insert(point_idx_in_bucket)
                    # else: # Nếu điểm không phải core, đảm bảo nó không có trong BST (quan trọng nếu điểm mất tư cách core)
                    #     current_bst.delete(point_idx_in_bucket) # Cần hàm delete trong BST

    def _link_all_points(self):
        for i in list(self.core_points): # Duyệt bản sao để tránh lỗi thay đổi kích thước set
            self.link_core_point(i)
        for i in list(self.non_core_points):
            self.link_non_core_point(i)

    def link_core_point(self, point_index: int, new_point=False):
        candidates_to_check: Set[int] = set()
        point_data = self.data[point_index]

        for j in range(self.t):
            this_hash_value = self.hash_functions[j].apply(point_data)
            
            bucket_list = self.hash_bucket_lists[j].get(this_hash_value, []) # Lấy danh sách đầy đủ
            bucket_bst = self.hash_bucket_bsts[j].get(this_hash_value) # Lấy BST (có thể None nếu bucket không có core point)

            if new_point:
                # Vẫn duyệt danh sách để tìm core point đầu tiên phù hợp với logic cũ
                # BST không giúp tìm "core point đầu tiên được chèn"
                # Tuy nhiên, nếu chỉ cần nối với *một* core point bất kỳ, BST có thể giúp
                for i in reversed(bucket_list): # Duyệt ngược danh sách
                    if i in self.core_points and i != point_index:
                        self.forest.link(point_index, i)
                        # print(f"Linking new core {point_index} to existing core {i} in bucket of hash {this_hash_value}")
                        break # Nối với core point đầu tiên tìm thấy
                    elif i != point_index : # Không thêm chính nó vào candidate
                        candidates_to_check.add(i)
            else: # Not a new point, use BST for pre/next
                pre, _next = None, None
                if bucket_bst: # Chỉ tìm kiếm nếu có BST (tức là có core points trong bucket)
                    pre_val = bucket_bst.searchlower(point_index)
                    next_val = bucket_bst.searchhigher(point_index)
                    pre = pre_val if pre_val != 'NULL' else None
                    _next = next_val if next_val != 'NULL' else None
                
                # Thu thập candidates_to_check từ danh sách đầy đủ
                for i in bucket_list:
                    if i not in self.core_points and i != point_index:
                        candidates_to_check.add(i)
        
                must_link_both = False
                if (_next is not None and pre is not None and
                        pre in self.forest.nodes and # Kiểm tra node tồn tại
                        _next in self.forest.nodes[pre].neighbors):
                    self.forest.cut(pre, _next)
                    must_link_both = True

                if pre is not None and (must_link_both or True): # Luôn link với pre nếu pre tồn tại
                    self.forest.link(point_index, pre)
                if _next is not None and must_link_both : # Chỉ link với _next nếu must_link_both
                    self.forest.link(point_index, _next)


        for i in candidates_to_check:
            if i in self.non_core_points: # Chỉ link lại các non-core points
                self.link_non_core_point(i)

    def link_non_core_point(self, point_index: int):
        if point_index not in self.data or point_index not in self.forest.nodes: return # Điểm không tồn tại
        if len(self.forest.nodes[point_index].neighbors) > 0:
            return

        point_data = self.data[point_index]
        for i, hash_fn in enumerate(self.hash_functions):
            hash_val = hash_fn.apply(point_data)
            bucket_list = self.hash_bucket_lists[i].get(hash_val, []) # Dùng list để tìm core point
            for j_idx in bucket_list:
                if j_idx in self.core_points:
                    self.forest.link(point_index, j_idx)
                    return

    def unlink_non_core_point(self, point_index: int):
        if point_index not in self.data or point_index not in self.forest.nodes: return
        if len(self.forest.nodes[point_index].neighbors) > 0:
            for neighbor_idx in list(self.forest.nodes[point_index].neighbors):
                self.forest.cut(point_index, neighbor_idx) # Sửa thứ tự cut

    def add_point(self, point: np.ndarray) -> int:
        index = self.forest.add()
        self.data[index] = point
        self._insert_to_bucket_lists(point, index) # Thêm vào danh sách bucket trước

        # Xác định lại các core points và xây dựng lại BSTs
        # Cách tiếp cận đơn giản: gọi lại hàm xác định toàn bộ
        # Cách tối ưu hơn: chỉ cập nhật những bucket bị ảnh hưởng
        
        # --- Bắt đầu phần xác định core points bị ảnh hưởng ---
        affected_buckets_info = [] # List of (hash_func_idx, hash_val)
        for j_hash_func_idx in range(self.t):
            hash_val = self.hash_functions[j_hash_func_idx].apply(point)
            affected_buckets_info.append((j_hash_func_idx, hash_val))

        potential_new_core_from_this_point = set()
        is_new_point_core = False

        for j_hash_func_idx, hash_val in affected_buckets_info:
            bucket_list = self.hash_bucket_lists[j_hash_func_idx].get(hash_val, [])
            if len(bucket_list) >= self.minP: # Điểm mới có thể làm cho chính nó thành core
                is_new_point_core = True
            if len(bucket_list) == self.minP: # Điểm mới có thể làm các điểm khác trong bucket này thành core
                for pt_idx in bucket_list:
                    if pt_idx != index: # Không xét chính điểm mới
                         potential_new_core_from_this_point.add(pt_idx)
        
        if is_new_point_core:
            potential_new_core_from_this_point.add(index)
        
        newly_identified_core = potential_new_core_from_this_point - self.core_points
        
        if not newly_identified_core and not is_new_point_core: # Điểm mới không phải core và không làm điểm nào khác thành core
            self.non_core_points.add(index)
            self.link_non_core_point(index)
        else:
            # Cập nhật tập core_points và non_core_points
            self.core_points.update(newly_identified_core)
            self.non_core_points.difference_update(newly_identified_core)
            if index in self.core_points and index in self.non_core_points: # Đảm bảo index không ở cả hai
                self.non_core_points.remove(index)


            # Cập nhật BSTs cho các bucket bị ảnh hưởng và chứa core points mới
            for pt_new_core in newly_identified_core:
                pt_data = self.data[pt_new_core]
                for j_idx in range(self.t):
                    hv = self.hash_functions[j_idx].apply(pt_data)
                    if hv not in self.hash_bucket_bsts[j_idx]:
                        self.hash_bucket_bsts[j_idx][hv] = BinarySearchTree()
                    self.hash_bucket_bsts[j_idx][hv].insert(pt_new_core)

                # Nếu điểm này trước đó là non-core, unlink nó
                self.unlink_non_core_point(pt_new_core)
                self.link_core_point(pt_new_core, new_point=(pt_new_core == index and len(newly_identified_core) == 1))
        return index


    def get_cluster(self, index: int) -> int: # Sửa lại để trả về int
        if index not in self.forest.nodes or not self.forest.nodes[index].neighbors:
            return -1 # Hoặc một giá trị đặc biệt khác cho không thuộc cluster nào
        return self.forest.root(index)

if __name__ == '__main__':
    for i in range(5): # Giảm số lần lặp để nhanh hơn
        # Tạo dữ liệu ngẫu nhiên với shape (số điểm, số chiều)
        num_points = 100 # Giảm số điểm
        num_dimensions = 4
        data_list = [np.random.randint(0, 10, size=(num_dimensions,)) for _ in range(num_points)]
        initial_data_np = np.array(data_list)

        minP = 3
        t_hash_functions = 2
        eps_val = 1.5

        print(f"\n--- Iteration {i+1} ---")
        dbscan = DynamicDBSCAN(minP, t_hash_functions, eps_val, initial_data_np)
        
        new_point_data = np.array([1, 2, 3, 4]) # Điểm mới để thêm
        print(f"Adding point: {new_point_data}")
        added_point_index = dbscan.add_point(new_point_data)
        print(f"Added point index: {added_point_index}")

        print('Core points:')
        print(sorted(list(dbscan.core_points)))

        print('Non-core points:')
        print(sorted(list(dbscan.non_core_points)))

        # print("Forest structure (first few components):")
        # dbscan.forest.print_forest() # Có thể rất dài, cẩn thận khi in

        # Lấy cluster cho một vài điểm
        # points_to_check_cluster = list(dbscan.data.keys())[:5] # Lấy 5 điểm đầu tiên
        # if added_point_index not in points_to_check_cluster:
        #     points_to_check_cluster.append(added_point_index)

        # for pt_idx in points_to_check_cluster:
        #     if pt_idx in dbscan.data: # Kiểm tra điểm còn tồn tại
        #         cluster_id = dbscan.get_cluster(pt_idx)
        #         print(f"Point {pt_idx} belongs to cluster representative {cluster_id}")
        #     else:
        #         print(f"Point {pt_idx} no longer in dataset.")