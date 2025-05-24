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

class List:
    def __init__(self):
        self.head = self.tail = None

    def add_tail(self, x):
        p = Node(x)
        if self.head is None:
            self.head = self.tail = p
        else:
            self.tail.next = p
            self.tail = p

    def delete_list(self):
        self.head = self.tail = None  # Python's garbage collector will clean up

class Hashtable:
    def __init__(self, m):
        self.M = m  # kích thước bảng băm
        self.n = 0  # số phần tử hiện có
        self.table = [List() for _ in range(m)]

    def hash(self, maso):
        return maso % self.M

    def insert(self, x):
        if (self.n + 1) / self.M > LOAD:
            return 
        index = self.hash(x.maso)
        self.table[index].add_tail(x)
        self.n += 1

    def print(self):
        for i in range(self.M):
            p = self.table[i].head
            while p:
                print(p.data, end=" ")
                p = p.next
            print()

    def delete(self):
        for lst in self.table:
            lst.delete_list()
        self.table = []
        self.M = 0
        self.n = 0

def input_hocsinh():
    maso = int(input())
    hoten = input().strip()
    namsinh = int(input())
    gioitinh = int(input())
    tbk = float(input())
    return Hocsinh(maso, hoten, namsinh, gioitinh, tbk)

# --- MAIN ---
def main():
    m = int(input())
    hashtable = Hashtable(m)
    n = int(input())
    for _ in range(n):
        hs = input_hocsinh()
        hashtable.insert(hs)
    hashtable.print()
    hashtable.delete()

if __name__ == "__main__":
    main()
