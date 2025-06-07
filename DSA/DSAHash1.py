from typing import Optional
c = 0.7
class Hocsinh:
    def __init__(self, Maso):
        self.Maso = Maso
    def __eq__(self, other):
        if isinstance(other, Hocsinh):
            return self.Maso == other.Maso
        return False
class HashTable:
    class LinkedList:
        def __init__(self):
            self.head = None
        class Node:
            def __init__(self, obj : Optional['Hocsinh']):
                self.obj = obj
                self.next = None
        def is_empty(self):
            return self.head is None
        def insert(self, obj : Optional['Hocsinh']):
            if self.is_empty():
                self.head = self.Node(obj)
            else:
                new_node = self.Node(obj)
                new_node.next = self.head
                self.head = new_node
        def search(self, index : int):
            current = self.head
            while current is not None:
                if current.obj.Maso == index:
                    return current.obj
                current = current.next
            return False
    def __init__(self, size):
        self.size = size
        self.table = [self.LinkedList() for _ in range(size)]
        self.total = 0
    def _hash_fuction(self, key):
        return key % self.size
    def insert(self, obj : Optional['Hocsinh']):
        if (self.total + 1) / self.size > c:
            return 0
        index = self._hash_fuction(obj.Maso)
        chain = self.table[index]
        if chain.is_empty():
            chain.insert(obj)
        else:
            if chain.search(obj.Maso):
                return 0
            chain.insert(obj)
            self.total += 1
        return 1
    def __getitem__(self, maso):
        return self.table[self._hash_fuction(maso)].search(maso)
#     def display(self):
#         print(f"--- Bảng băm (Kích thước: {self.size}, Số phần tử: {self.total}, Hệ số tải: {self.total/self.size:.2f}) ---")
#         for i, chain in enumerate(self.table):
#             print(f"Bucket {i}: {chain}")
#         print("-" * 40)
    
# if __name__ == "__main__":
#     # Tạo một bảng băm với kích thước 5
#     # Với MAX_LOAD_FACTOR = 0.7, bảng băm này có thể chứa tối đa 5 * 0.7 = 3.5 => 3 phần tử
#     hash_table = HashTable(size=5)

#     hs1 = Hocsinh(101)
#     hs2 = Hocsinh(202)
#     hs3 = Hocsinh(106) 
#     hs4 = Hocsinh(303)
#     hs5_duplicate_maso = Hocsinh(101) # Maso trùng với hs1

#     print("--- Bắt đầu thêm học sinh ---")

#     result = hash_table.insert(hs1)
#     print(f"Kết quả thêm {hs1.Maso}: {result}") 
#     hash_table.display()    

#     result = hash_table.insert(hs2)
#     print(f"Kết quả thêm {hs2.Maso}: {result}") 
#     hash_table.display()

#     result = hash_table.insert(hs3) 
#     print(f"Kết quả thêm {hs3.Maso}: {result}") # Mong đợi: 1
#     hash_table.display()

#     result = hash_table.insert(hs4)
#     print(f"Kết quả thêm {hs4.Maso}: {result}") # Mong đợi: 0
#     hash_table.display()

#     result = hash_table.insert(hs5_duplicate_maso)
#     print(f"Kết quả thêm (trùng Maso) {hs5_duplicate_maso.Maso}: {result}") # Mong đợi: 0
#     hash_table.display()

        
