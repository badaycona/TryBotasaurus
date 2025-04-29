class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def pushleft(self, val):
        node = Node(val)
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node

    def push(self, val):
        node = Node(val)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = self.tail.next

    def insert_after(self, a, b):
        cur = self.head
        while cur:
            if cur.val == a:
                break
            cur = cur.next
        node = Node(b)
        if not cur:
            # a không tồn tại, chèn b vào đầu
            self.pushleft(b)
        else:
            node.next = cur.next
            cur.next = node
            if cur == self.tail:
                self.tail = node

    def delete(self, val):
        if not self.head:
            return
        if self.head.val == val:
            self.head = self.head.next
            if not self.head:
                self.tail = None
            return
        prev, cur = self.head, self.head.next
        while cur:
            if cur.val == val:
                prev.next = cur.next
                if cur == self.tail:
                    self.tail = prev
                return
            prev, cur = cur, cur.next
    def popleft(self):
        if self.head:
            self.head = self.head.next
            if not self.head:
                self.tail = None

    def show(self):
        if not self.head:
            print("blank")
            return
        cur = self.head
        while cur:
            print(cur.val, end = ' ')
            cur = cur.next

import sys
line = list(sys.stdin.read().strip().split())
i = 0
n = len(line)
ll = LinkedList()

while i < n:
    cur = line[i]
    if cur == '0':
        ll.pushleft(line[i+1])
        i += 2
    elif cur == '1':
        ll.push(line[i+1])
        i += 2
    elif cur == '2':
        ll.insert_after(line[i+1], line[i+2])
        i += 3
    elif cur == '3':
        ll.delete(line[i+1])
        i += 2
    elif cur == '5':
        ll.popleft()
        i += 1
    else:
        i = n
        break

ll.show()
