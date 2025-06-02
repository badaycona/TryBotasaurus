
LOAD = 0.7
class Hocsinh:
    def __init__(self, maso, hoten, namsinh, gioitinh, tbk):
        self.maso = maso
        self.hoten = hoten
        self.namsinh = namsinh
        self.gioitinh = gioitinh
        self.tbk = tbk

    def __str__(self):
        return f"[{self.maso}, {self.hoten} , {self.namsinh}, {self.gioitinh}, {self.tbk:g}]"

class Node:
    def __init__(self, data: Hocsinh):
        self.data = data
        self.next = None
class Hashtable:
    def __init__(self, m_size: int):
        self.M = m_size
        self.n = 0 
        self.table = [None] * self.M


    def hash(self, maso: int) -> int:
        return maso % self.M

    def search(self, maso: int) -> Node | None:
            
        index = self.hash(maso)
        
        current_node = self.table[index]
        
        while current_node is not None:
            if current_node.data.maso == maso:
                return current_node
            current_node = current_node.next
            
        return None
    def insert(self, hs):
        if (self.n + 1) / self.M > LOAD:
            return None
       
        index = self.hash(hs.maso)
        if self.table[index] is None:
            self.table[index] = Node(hs)
        else:
            current = self.table[index]
            prev = None
            while current:
                if current.data.maso == hs.maso:
                    current.data = hs # CẬP NHẬT DỮ LIỆU
                    # Không tăng self.n vì đây là cập nhật, không phải thêm mới
                    return True # Xử lý xong (cập nhật)
                prev = current
                current = current.next
            # Nếu duyệt hết mà không trùng key, thêm vào cuối (sau prev)
            if prev: # prev là Node cuối cùng trước đó
                prev.next = Node(hs)
        self.n += 1


def input_hocsinh_from_std() -> Hocsinh:
    maso = int(input())
    hoten = input().strip()
    namsinh = int(input())
    gioitinh = int(input())
    tbk = float(input())
    return Hocsinh(maso, hoten, namsinh, gioitinh, tbk)

def main():
    m = int(input())
    hashtable = Hashtable(m)

    for i in range(m):
        k = int(input())
        for _ in range(k):
            hs = input_hocsinh_from_std()
            hashtable.insert(hs)
            
    n  = int(input())
        
    for _ in range(n):
        maso_to_search = int(input())
        found_node = hashtable.search(maso_to_search)

        if found_node is None:
            print('KHONG TIM THAY')
        else:
            hs_data = found_node.data
            print(hs_data)
        
if __name__ == "__main__":
    main()