s = input()
l = [i for i in s]
for i in range(len(l)):
    for j in range(i, len(l)):
        if l[i] > l[j]:
            l[i], l[j] = l[j], l[i]
print(''.join(l))