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

def delete_hashtable(ht: Hashtable):
    ht.table = []
    ht.M = 0
    ht.n = 0

def Search(ht: Hashtable, maso: int, nprob_ref: list) -> int:
    if ht.M == 0:
        nprob_ref[0] = 0 
        return -1

    key = maso
    m_size = ht.M

    for i in range(m_size): 
        nprob_ref[0] = i + 1 
        
        current_pos = ((key % m_size) + (i * i)) % m_size

        if ht.table[current_pos].Maso == key:
            return current_pos
        
        if ht.table[current_pos].Maso == EMPTY:
            return -1
        

    return -1

if __name__ == '__main__':
    m = int(input())
    hashtable_instance = create_hashtable_from_input(m)

    n_searches = int(input())
    for _ in range(n_searches):
        k_to_search = int(input())
        nprob_list = [0]
        
        result_index = Search(hashtable_instance, k_to_search, nprob_list)
        

        
        if result_index > -1:

            nprob_list_corrected = [0]
            
            key_search = k_to_search
            m_size_search = hashtable_instance.M
            found_idx_corrected = -1

            if m_size_search > 0:
                for attempt_idx in range(m_size_search):
                    nprob_list_corrected[0] = attempt_idx # Số lần dò thêm
                    pos_corrected = ((key_search % m_size_search) + (attempt_idx * attempt_idx)) % m_size_search
                    
                    if hashtable_instance.table[pos_corrected].Maso == key_search:
                        found_idx_corrected = pos_corrected
                        break 
                    if hashtable_instance.table[pos_corrected].Maso == EMPTY:
             
                        break 
    

            if found_idx_corrected > -1:
                 print(f"THAM DO {nprob_list_corrected[0]}")
            else:
                print("KHONG TIM THAY")

        else: 
            print("KHONG TIM THAY")
            
    delete_hashtable(hashtable_instance)