t = int(input())
ans = []
for i in range(t):
    n, k = map(int,input().split())
    A = list(map(int,input().split()))
    d = {}
    c1 = c2 = 0
    for i in A:
        if i in d:
            d[i] +=1
            c2 += 1
            c1 -= 1
        else:
            d[i] = 1
            c1 += 1
    c1 = c2 = 0
    for i in d.values():
        if i > 1:
            c2 += 1
        else:
            c1 += 1
    if 2*k <= c1 + 2*c2 and len(d) >= 2*k:
        ans.append(1)
    else:
        ans.append(0)
for i in ans:
    if i:
        print('YES')
    else:
        print('NO')

        