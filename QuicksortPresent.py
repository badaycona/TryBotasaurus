def quick(l):   
    if l:
        pivot = l[0]
        left = [i for i in l[1:] if i < pivot]
        right = [i for i in l[1:] if i > pivot]
        mid = [i for i in l if i == pivot]
        return quick(left) + mid + quick(right)
    else:
        return l
def binarysearch(l, x):
    left, right = 0, len(l) - 1
    while left <= right:
        mid = (right + left) // 2
        if l[mid] == x:
            return True
        elif l[mid] > x:
            right = mid - 1
        else:
            left = mid + 1
    return False
n, q = map(int,input().split())
d = list(map(int,input().split()))
d = quick(d)
for i in range(q):
    x = int(input())
    if binarysearch(d, x):
        print('YES')
    else:
        print('NO')
