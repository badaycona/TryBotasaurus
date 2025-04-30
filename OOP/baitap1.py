from collections import defaultdict, deque
import sys

class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map = {}  # Cho phép nhiều node trùng giá trị

    def push(self, val):
        node = Node(val)
        prev = self.tail.prev

        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

        self.map[val].append(node)

    def pushleft(self, val):
        node = Node(val)
        nxt = self.head.next

        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

        self.map[val].appendleft(node)

    def insert_after(self, cur_val, val):
    # Nếu không tồn tại cur_val trong danh sách
        if cur_val not in self.map or not self.map[cur_val]:
            self.pushleft(val)
            return

    # Duyệt từ đầu đến node đầu tiên có giá trị cur_val
        cur = self.head.next
        while cur != self.tail:
            if cur.val == cur_val:
                break
            cur = cur.next

    # Nếu vì lý do nào đó không tìm được, thêm vào đầu
        if cur == self.tail:
            self.pushleft(val)
            return

    # Thêm node mới sau node tìm được
        node = Node(val)
        nxt = cur.next

        cur.next = node
        node.prev = cur
        node.next = nxt
        nxt.prev = node

        self.map[val].append(node)
    def delete(self, val):
        if val not in self.map or not self.map[val]:
            return
        node = self.map[val].popleft()
        node.prev.next = node.next
        node.next.prev = node.prev
        if not self.map[val]:
            del self.map[val]

    def popleft(self):
        if self.head.next == self.tail:
            return None
        node = self.head.next
        self.head.next = node.next
        node.next.prev = self.head
        self.map[node.val].remove(node)
        if not self.map[node.val]:
            del self.map[node.val]
        return node.val

    def show(self):
        if self.head.next == self.tail:
            print("blank")
            return
        cur = self.head.next
        while cur != self.tail:
            print(cur.val, end=' ')
            cur = cur.next
        print()
line = list(sys.stdin.read().strip().split())
i = 0
n = len(line)
ans = LinkedList()
while i < n:
    cur = line[i]
    if cur == '0':
        ans.pushleft(line[i + 1])
        i += 2
    elif cur == '1':
        ans.push(line[i + 1])
        i += 2
    elif cur == '2':
        ans.insert_after(line[i + 1], line[i + 2])
        i += 3
    elif cur == '3':
        ans.delete(line[i + 1])
        i += 2
    elif cur == '5':
        ans.popleft()
        i += 1
    else:
        i = n
        break
ans.show()
