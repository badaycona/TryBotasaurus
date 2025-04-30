from collections import deque
dq = deque()
n = int(input())
for i in range(n):
    k = input().split()
    if len(k) == 2:
        dq.append(k[1])
    elif k[0] == 'D':
        print(dq.popleft())
    else:
        print(dq[0])
for i in range(len(dq)):
    print(i, end = ' ')
    