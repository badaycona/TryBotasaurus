from collections import deque
s = input()
s = s.replace(':', '/')
stack = []
temp = ''
val, ops = [], []
i = 0
n = len(s)
def cal(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b
def pri(op):
    if op in ['+', '-']:
        return 1
    if op in ['*','/']:
        return 2
    return 0
while i < len(s):
    if s[i] == '(':
        ops.append(s[i])
    elif s[i].isdigit():
        temp = ''
        while i < n and s[i].isdigit():
            temp += s[i]
            i += 1
        val.append(int(temp))
        i -= 1
    elif s[i] == ')':
        while ops and ops[-1] != '(':
            b = val.pop()
            a = val.pop()
            op = ops.pop()
            val.append(cal(a, b, op))
        ops.pop()
    elif s[i] in '+-*/':
        while ops and pri(ops[-1]) >= pri(s[i]):
            b = val.pop()
            a = val.pop()
            op = ops.pop()
            val.append(cal(a, b, op))
        ops.append(s[i])
    i += 1
while ops:
    b = val.pop()
    a = val.pop()
    op = ops.pop()
    val.append(cal(a, b, op))
print(f'{val[0]:g}')