import random

def quickselect(arr, k):
    if len(arr) == 1:  # Nếu chỉ còn 1 phần tử, đó chính là kết quả
        return arr[0]

    pivot = random.choice(arr)  # Chọn pivot ngẫu nhiên

    # Chia mảng thành 2 phần:
    left = [x for x in arr if x <= pivot]  # Nhỏ hơn hoặc bằng pivot
    right = [x for x in arr if x > pivot]  # Lớn hơn pivot

    if k <= len(left):  # Nếu k nằm trong nhóm nhỏ hơn hoặc bằng
        return quickselect(left, k)
    else:  # Nếu k nằm trong nhóm lớn hơn
        return quickselect(right, k - len(left))

n = list(map(int,input().split()))
k = int(input())
print(quickselect(n, k))