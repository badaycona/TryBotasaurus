LOAD = 0.7
EMPTY = 0
DELETE = -1

class Hocsinh:
    def __init__(self, Maso=EMPTY, Hoten="", Namsinh=0, Gioitinh=False, TBK=0.0):
        self.Maso = Maso
        self.Hoten = Hoten
        self.Namsinh = Namsinh
        self.Gioitinh = Gioitinh  # True for male (1), False for female (0)
        self.TBK = TBK

class Hashtable:
    def __init__(self, m_size: int):
        self.M = m_size  
        self.n = 0       
        if m_size > 0:
            self.table = [Hocsinh(Maso=EMPTY) for _ in range(m_size)]
        else:
            self.table = [] 


def print_hashtable(ht: Hashtable):
    for i in range(ht.M):
        hs = ht.table[i]
        if hs.Maso > 0:
            print(f'[{hs.Maso},  {hs.Hoten}  , {int(hs.Gioitinh)}, {hs.Namsinh}, {hs.TBK:g}]')
        else:
            print(f"[{hs.Maso},    , , , ]")


def delete_hashtable(ht: Hashtable):
    ht.table = []
    ht.M = 0
    ht.n = 0

def input_hocsinh():
    maso = int(input())
    hoten = input() 
    namsinh = int(input())
    gioitinh_val = int(input()) # Đọc 0 hoặc 1
    gioitinh = bool(gioitinh_val)
    tbk = float(input())
    return Hocsinh(maso, hoten, namsinh, gioitinh, tbk)

def insert(ht: Hashtable, x: Hocsinh) -> int:
    if ht.M == 0: 
        return 0
        
    if (ht.n + 1) > (ht.M * LOAD):
        return 0  

    key = x.Maso
    m_size = ht.M

    for i in range(m_size): 
        current_pos = ((key % m_size) + i) % m_size

        if ht.table[current_pos].Maso == EMPTY or ht.table[current_pos].Maso == DELETE:
            ht.table[current_pos] = x
            ht.n += 1 
            return 1  
        elif ht.table[current_pos].Maso == key:
            return 0 
  
    return 0 

if __name__ == '__main__':
    m_param = int(input())
    hashtable_instance = Hashtable(m_param) 

    n_param = int(input())
    for _ in range(n_param):
        hocsinh_data = input_hocsinh()
        insert(hashtable_instance, hocsinh_data)
        
    print_hashtable(hashtable_instance)