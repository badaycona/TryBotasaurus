import sys
count = 0
i = 0
ans = []
def is_virus(i, j):
    if j + len_cur <= m: 
        flag = True
        for k in range(1, len_cur):
            if table[i][j + k] != cur[k]:
                flag = False
                break
        if flag:
            return True
    if i + len_cur <= n:
        flag2 = True
        for k in range(1, len_cur):
            if table[i + k][j] != cur[k]:
                flag2 = False
                break
        if flag2:
            return True
    return False
for line in sys.stdin:
    if count == 0:
        n, m, q = map(int, line.split())
        table = [['' for _ in range(m)] for i in range(n)]
    elif count < n + 1:
        table[i] = list(line.strip())
        i += 1
    else:
        cur = line.strip()
        len_cur = len(cur)
        found = False
        for i in range(n):
            for j in range(m):
                if table[i][j] == cur[0] and is_virus(i, j):
                    ans.append('1')
                    found = True
                    break
            if found:
                break
        if not found:
            ans.append('0')
    count += 1
print(''.join(ans))

