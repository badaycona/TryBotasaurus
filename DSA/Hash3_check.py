class Hocsinh:
    def __init__(self, maso, hoten, namsinh, gioitinh, tbk):
        self.maso = maso
        self.hoten = hoten
        self.namsinh = namsinh
        self.gioitinh = gioitinh
        self.tbk = tbk

    def __str__(self):
        return f"[{self.maso},  {self.hoten}  , {self.namsinh}, {self.gioitinh}, {self.tbk:g}]"

class Node:
    def __init__(self, hs):
        self.data = hs
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None 

    def add_tail(self, hs_data: Hocsinh):
        new_node = Node(hs_data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            if self.tail: 
                 self.tail.next = new_node
            else: 
                 self.head.next = new_node
            self.tail = new_node


class HashTable:
    def __init__(self, size):
        self.n = 0 
        self.M = size 
        self.table = [LinkedList() for _ in range(self.M)]

    def hash(self, maso):
        if self.M == 0: 
            return 0 
        return maso % self.M

    def insert(self, hs):
        index = self.hash(hs.maso)


        current = self.table[index].head
        while current:
            if current.data.maso == hs.maso:
                current.data = hs 
                return
            current = current.next
        
        self.table[index].add_tail(hs)
        self.n += 1 

    def delete(self, maso_to_delete: int) -> int:
        if self.M == 0:
            return 0

        index = self.hash(maso_to_delete)
        
        linked_list_at_index = self.table[index]
        current = linked_list_at_index.head
        prev = None

        while current is not None:
            if current.data.maso == maso_to_delete:
                if prev is None:
                    linked_list_at_index.head = current.next
                    if linked_list_at_index.head is None:
                        linked_list_at_index.tail = None
                    elif current == linked_list_at_index.tail: 
                        linked_list_at_index.tail = prev 
                else:
                    prev.next = current.next
                    if current == linked_list_at_index.tail:
                        linked_list_at_index.tail = prev
                
                self.n -= 1 
                return 1
            
            prev = current
            current = current.next
            
        return 0 

    def print_hashtable(self): 
        for i in range(self.M):
            current_node = self.table[i].head
            output_nodes = []
            while current_node:
                output_nodes.append(str(current_node.data))
                current_node = current_node.next
            if output_nodes:
                print(" ".join(output_nodes))
            else:
                print()


def input_hocsinh() -> Hocsinh:
    maso = int(input())
    hoten = input().strip()
    namsinh = int(input())
    gioitinh_val = int(input()) 
    tbk = float(input())
    return Hocsinh(maso, hoten, namsinh, gioitinh_val, tbk)

def main():
    m_size = int(input())
    hashtable = HashTable(m_size)

    for _ in range(m_size): 
        k_items_in_bucket_group = int(input())
        for _ in range(k_items_in_bucket_group):
            hs = input_hocsinh()
            hashtable.insert(hs) 

    num_deletions = int(input())
    for _ in range(num_deletions):
        maso_to_delete = int(input())
        result = hashtable.delete(maso_to_delete)
        if result == 0:
            print('KHONG XOA DUOC')

    hashtable.print_hashtable()

if __name__ == "__main__":
    main()