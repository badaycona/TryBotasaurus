import random
def Quickselect(l : list[int], k : int ) -> int :
    first = l[0]
    mid = l[len(l) // 2]
    last = l[len(l) - 1]
    pivot = sorted([first, mid, last])[1]
    left = [i for i in l if i < pivot]
    right = [i for i in l if i >= pivot]
    
    if k == len(left) + 1:
        return pivot
    elif k < len(left) + 1:
        return Quickselect(left, k)
    else:
        return Quickselect(right, k - len(left))

def generate_testcase(left, right, rang):
    return [random.randint(left, right) for i in range(random.randint(1,rang))]

l = generate_testcase(1, 100, 20)
a = random.randint(1, 5)
print(l)
print(a)
print(Quickselect(l, a))