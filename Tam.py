def task():
    array = list(map(int, input().split()))
    data_max = [None]*2
    data_min = [None]*2
    for i in range(2):
        if array == []:
            data_max[i] = data_max[i-1]
        else:
            data_max[i] = max(array)
            array = [x for x in array if x != data_max[i]]
    for i in range(2):
        if array == []:
            data_min[i] = data_max[i]
        else:
            data_min[i] = min(array)
            array = [x for x in array if x != data_min[i]]
    # print(data_max)
    # print(data_min)
    return(data_max[0] - data_min[0] + data_max[1] - data_min[1])

def main():
    T = int(input())
    S = [None]*T
    for i in range(T):
        S[i] = task()
    for i in range(T):
        print(S[i])

main()