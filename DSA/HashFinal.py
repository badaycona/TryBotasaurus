n, q = map(int, input().split())
stored = {}
for i in range(n):
    s, t = input().split()
    stored[s] = t
for i in range(q):
    x = input()
    if x in stored:
        print(stored[x])
    else:
        print('Chua Dang Ky!')