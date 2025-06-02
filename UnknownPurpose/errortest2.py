class SinhVien:
    def __init__(self, ma_so, ho_ten, nam_sinh, gioi_tinh, diem_toan, diem_ly, diem_hoa):
        self.ma_so = ma_so
        self.ho_ten = ho_ten
        self.nam_sinh = nam_sinh
        self.gioi_tinh = gioi_tinh
        self.diem_toan = diem_toan
        self.diem_ly = diem_ly
        self.diem_hoa = diem_hoa
        self.diem_trung_binh = (diem_toan + diem_ly + diem_hoa) / 3

    def __str__(self):
        # Định dạng điểm trung bình để hiển thị nhiều nhất ba số sau dấu thập phân, nếu có
        diem_tb = f"{self.diem_trung_binh:.3f}".rstrip('0').rstrip('.')
        return f"{self.ma_so}\t{self.ho_ten}\t{self.nam_sinh}\t{self.gioi_tinh}\t{self.diem_toan:g}\t{self.diem_ly:g}\t{self.diem_hoa:g}\t{diem_tb}"

# Nhập thông tin sinh viên
ma_so = input()
ho_ten = input()
nam_sinh = input()
gioi_tinh = input()
diem_toan = float(input())
diem_ly = float(input())
diem_hoa = float(input())

# Tạo đối tượng SinhVien
sv = SinhVien(ma_so, ho_ten, nam_sinh, gioi_tinh, diem_toan, diem_ly, diem_hoa)

# Xuất thông tin sinh viên
print(sv)   