import sys
from collections import deque, defaultdict
# class Node:
#     def __init__(self, val = 0, next = None):
#         self.val = val
#         self.next = next
        
# class LinkedList:
#     def __init__(self, head = None, tail = None):
#         self.head = head
#         self.tail = tail
#     def pushhead(self, val):
#         new = Node(val)
#         if not self.head:
#             self.head = new
#             self.tail = new
#         else:
#             new.next = self.head
#             self.head = new
#     def pushtail(self, val):
#         new = Node(val)
#         if not self.head:
#             self.head = new
#             self.tail = new
#         else:
#             self.tail.next = new        
#             self.tail = self.tail.next
#     def __str__(self):
#         s = ''
#         dummy = self.head
#         while dummy:
#             s += str(dummy.val) + ' '
#             dummy = dummy.next
#         return s
# ans = LinkedList()
dq = deque()
line = list(sys.stdin.read().strip().split())
i = 0
s = defaultdict(int)
n = len(line)
while i < n:
    cur = line[i]
    if cur == '0':
        val = line[i + 1]
        s[val] += 1
        dq.appendleft(val)
        i += 2
    elif cur == '1':
        val = line[ i + 1]
        s[val] += 1
        dq.append(val)
        i += 2
    elif cur == '2':
        val = line[i + 2]
        cor = line[i + 1]
        if cor in s and  s[cor] > 0:
            j = dq.index(cor)
            dq.rotate(-j - 1)
            dq.appendleft(val)
            dq.rotate(j + 1)
        else:
            dq.appendleft(val)
        s[val] += 1
        i += 3
    elif cur == '3':
        val = line[i + 1]
        if val in s and s[val] > 0:
            j = dq.index(val)
            dq.rotate(-j)
            dq.popleft()
            dq.rotate(j)
            s[val] -= 1
        i += 2
    elif cur == '5':
        if dq:
            s[dq.popleft()] -= 1
        i += 1
    else:
        i = n
        break
sys.stdout.write(' '.join(dq) if dq else 'blank')
# for i in range(0, len(line), 2):
#     if line[i] == 0:
#         ans.pushhead(line[i + 1])
#     else:
#         ans.pushtail(line[i + 1])
# print(ans)
