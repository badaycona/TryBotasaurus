def merge_sort(arr, start, end):
    if start >= end:
        return  

    mid = (start + end) // 2
    merge_sort(arr, start, mid)  # Sắp xếp nửa trái
    merge_sort(arr, mid + 1, end)  # Sắp xếp nửa phải
    merge(arr, start, mid, end)  # Gộp hai phần đã sắp xếp
    print(f"Sorted subarray from index {start} to {end}: {arr[start:end+1]}")  # Lưu lại

def merge(arr, start, mid, end):
    left = arr[start:mid+1]
    right = arr[mid+1:end+1]

    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
n = int(input())
l = list(map(int, input().split()))
print()
merge_sort(l, 0, n - 1)