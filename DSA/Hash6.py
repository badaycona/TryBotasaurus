LOAD = 0.7
EMPTY = 0
DELETE = -1

class Hocsinh:
    def __init__(self, Maso=EMPTY, Hoten="", Gioitinh=False, Namsinh=0, TBK=0.0):
        self.Maso = Maso
        self.Hoten = Hoten
        self.Namsinh = Namsinh
        self.Gioitinh = Gioitinh
        self.TBK = TBK

class Hashtable:
    def __init__(self, m_size: int):
        self.M = m_size
        self.n = 0
        if m_size > 0:
            self.table = [Hocsinh(Maso=EMPTY) for _ in range(m_size)]
        else:
            self.table = []

def create_hashtable_from_input(m_size: int):
    ht = Hashtable(m_size)
    for i in range(m_size):
        maso_val = int(input())
        if maso_val == EMPTY or maso_val == DELETE:
            ht.table[i] = Hocsinh(Maso=maso_val)

            _ = input() 
            _ = input() 
            _ = input() 
            _ = input() 
        else:
            hoten_val = input()
            gioitinh_int_val = int(input())
            namsinh_val = int(input())
            tbk_val = float(input())
            ht.table[i] = Hocsinh(maso_val, hoten_val, bool(gioitinh_int_val), namsinh_val, tbk_val)
            if maso_val > 0: 
                ht.n +=1
    return ht

def print_hashtable(ht: Hashtable):
    for i in range(ht.M):
        hs = ht.table[i]
        if hs.Maso > 0:
            print(f'[{hs.Maso},  {hs.Hoten}  , {int(hs.Gioitinh)}, {hs.Namsinh}, {hs.TBK:g}]')
        else:
            print(f"[{hs.Maso},    , , , ]")

def delete_hashtable_cleanup(ht: Hashtable):
    ht.table = []
    ht.M = 0
    ht.n = 0

def Delete(ht: Hashtable, maso: int, nprob_ref: list) -> int:

    if ht.M == 0:
        nprob_ref[0] = 0
        return 0

    key = maso
    m_size = ht.M

    for i in range(m_size): 
        nprob_ref[0] = i 
        
        current_pos = ((key % m_size) + (i * i)) % m_size

        if ht.table[current_pos].Maso == key:
            ht.table[current_pos].Maso = DELETE
            ht.table[current_pos].Hoten = "" 
            ht.table[current_pos].Namsinh = 0
            ht.table[current_pos].Gioitinh = False
            ht.table[current_pos].TBK = 0.0
            ht.n -= 1 
            return 1 
        
        if ht.table[current_pos].Maso == EMPTY:
     
            return 0 
        

    return 0

if __name__ == '__main__':
    m = int(input())
    hashtable_instance = create_hashtable_from_input(m)

    n_deletes = int(input())
    for _ in range(n_deletes):
        k_to_delete = int(input())
        nprob_list = [0] 
        
        delete_success = Delete(hashtable_instance, k_to_delete, nprob_list)
        
        if delete_success:
 
            print(f"THAM DO {nprob_list[0]}")
        else:
            print("KHONG XOA DUOC")
            
    print_hashtable(hashtable_instance)
    delete_hashtable_cleanup(hashtable_instance)