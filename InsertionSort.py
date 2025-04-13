def mergesort(k : list, left, right):
    if left >= right:
        return 
    mid = (right - left) // 2
    mergesort(k, left , mid)
    mergesort(k, mid + 1, right)
    merge(k, left, mid, right)
    print(k, left, right)
def merge(k, left, mid, right):
    i = j = 0
    ind = left
    leftpart = k[left : mid + 1]
    rightpart = k[mid + 1 : right + 1]
    while i < len(leftpart) and j < len(rightpart):
        if leftpart[i] > rightpart[j]:
            k[ind] = rightpart[j]
            j += 1
        else:
            k[ind] = leftpart[i]
            i += 1
        ind += 1

    while i < len(leftpart):
        k[ind] = leftpart[i]
        i += 1
        ind += 1

    while j < len(rightpart):
        k[ind] = rightpart[j]
        j += 1
        ind += 1
n = int(input())
l = list(map(int, input().split()))
print()
mergesort(l, 0, n - 1)