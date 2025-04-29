class Linked:
    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail
    def push(self, node):
        if not self.head and not self.tail:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = self.tail.next
class Node:
    def __init__(self, a, b, next = None):
        self.a = float(a)
        self.b = int(b)
        self.next = next
    def __str__(self):
        a, b = self.a, self.b
        s = ''
        if a == 0:
            s += ''
        elif a > 0:
            if b == 0:
                s += f'+{a:g}'
            elif a == 1 and b == 1:
                s += '+x'
            elif a == 1:
                s += f'+x^{b}'
            elif b == 1:
                s += f'+{a:g}x'
            else:
                s += f'+{a:g}x^{b}'
        else:
            if b == 0:
                s += f'{a:g}'
            elif a == -1 and b == 1:
                s += '-x'
            elif a == -1:
                s += f'-x^{b}'
            elif b == 1:
                s += f'{a:g}x'
            else:
                s += f'{a:g}x^{b}'
        return s
n = int(input())
s = ''
storage = Linked()
ans = 0
for i in range(n):
    storage.push(Node(*map(float, input().split())))
    s += str(storage.tail)
x = float(input())
dummy = storage.head
for i in range(n):
    ans += dummy.a * (x ** dummy.b)
    dummy = dummy.next
if s and s[0] == '+':
    s = s[1:]
print('Da thuc vua nhap la:',s if s else 0)
print(f'Voi x={x:g}, gia tri da thuc la: {ans:.2f}')