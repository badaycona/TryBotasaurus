def mergesort(arr, start, end):
    if start >= end:
        return
    mid = (start + end) // 2
    left = mergesort(arr, start, mid)
    right = mergesort(arr, mid + 1, end)
    merge(arr, start, mid, end)
    for i in range(len(arr)):
        if i == start:
            print('[', end = ' ')
        print(arr[i], end = ' ')
        if i == end:
            print(']', end = ' ')
    print()
def merge(arr, start, mid, end):
    leftpart = arr[start : mid + 1]
    rightpart = arr[mid + 1 : end + 1]
    i = j = 0
    k = start
    while i < len(leftpart) and j < len(rightpart):
        if leftpart[i] < rightpart[j]:
            arr[k] = leftpart[i]
            k += 1
            i += 1
        else:
            arr[k] = rightpart[j]
            k += 1
            j += 1
    while i < len(leftpart):
        arr[k] = leftpart[i]
        k += 1
        i += 1
    while j < len(rightpart):
        arr[k] = rightpart[j]
        k += 1
        j += 1

n = int(input())
l = list(map(int,input().split()))

mergesort(l, 0, n - 1)
