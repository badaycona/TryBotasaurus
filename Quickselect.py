import random
def Quickselect(l : list[int], k : int ) -> int:
    pivot = sorted([l[0], l[len(l) - 1], l[len(l) // 2]])[1]
    left = [i for i in l if i < pivot]
    right = [i for i in l if i >= pivot]
    if k == len(left) + 1:
        return pivot
    elif k < len(left) + 1:
        return Quickselect(left, k)
    else:
        return Quickselect(right, k - len(left))

def generate_testcase(left, right, ran):
    return [random.randint(left, right) for _ in range(random.randint(1, ran))]
l = generate_testcase(0, 100, 20)
k = random.randint(1, len(l))
print(l)
print(k)
print(Quickselect(l, k))