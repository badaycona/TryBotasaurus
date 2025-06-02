import sys
LOAD = 0.7

class Hocsinh:
    def __init__(self, maso, hoten, namsinh, gioitinh, tbk):
        self.maso = maso
        self.hoten = hoten
        self.namsinh = namsinh
        self.gioitinh = gioitinh
        self.tbk = tbk

    def __str__(self):
        return f"[{self.maso},  {self.hoten}  , {self.gioitinh}, {self.namsinh}, {self.tbk:g}]"

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    def insert(self, node):
        if not self.head:
            self.head = self.tail = node
            return
        self.tail.next = node
        self.tail = node
        return
class HashTable:
    def __init__(self, m):
        self.M = m  # kích thước bảng băm
        self.n = 0  # số phần tử hiện có
        self.table = [LinkedList() for _ in range(m)]

    def hash(self, maso):
        return maso % self.M

    def insert(self, x):
        if (self.n + 1) / self.M > LOAD:
            return 
        index = self.hash(x.maso)
        self.table[index].insert(Node(x))
        self.n += 1
    def search(self, maso: int) -> Node | None:
        if self.M == 0:
            return None
            
        index = self.hash(maso)
        
        if index < 0 or index >= self.M: # Should not happen with maso % M if M > 0
            return None

        list_to_search = self.table[index]
        
        current_node = list_to_search.head
        
        while current_node is not None:
            if current_node.data.maso == maso:
                return current_node
            current_node = current_node.next
            
        return None


def input_hocsinh_from_std() -> Hocsinh:
    maso = int(sys.stdin.readline())
    hoten = sys.stdin.readline().strip() 
    gioitinh = int(sys.stdin.readline())
    namsinh = int(sys.stdin.readline())
    tbk = float(sys.stdin.readline())
    return Hocsinh(maso, hoten, namsinh, gioitinh, tbk)

def main():
    m = int(sys.stdin.readline())
    table = HashTable(m)
    for _ in range(m):
        k = int(sys.stdin.readline())
        table.n += k
        for _ in range(k):
            hs = input_hocsinh_from_std()
            table.insert(hs)
    n = int(sys.stdin.readline())
    for _ in range(n):
        search_id = int(sys.stdin.readline())
        found_node = table.search(search_id)
        if found_node is None:
            print('KHONG TIM THAY')
        else:
            hs_data = found_node.data
            print(hs_data)

if __name__ == '__main__':
    main()
