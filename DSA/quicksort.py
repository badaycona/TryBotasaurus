def Quicksort(l : list[int]) -> list:
    if len(l) <= 1:
        return l
    pivot = sorted([l[0], l[~0], l[len(l) // 2]])[1]
    left = [i for i in l if i < pivot]
    right = [i for i in l if i >= pivot]
    return Quicksort(left) + Quicksort(right)

l = [1, 4, 2, 3, 6]
print(Quicksort(l)) 