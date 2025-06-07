from collections import deque
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
class Tree:
    def __init__(self):
        self.root = None
    def _add(node, value):
        if not node:
            return Node(value)
        if node.value > value:
            node.left =  Tree._add(node.left, value)
        else:
            node.right = Tree._add(node.right, value)
        return node
    def add(self, value):
        self.root = Tree._add(self.root, value)
    def Preorder(self):
        dq = deque()
        self.root
        dq.appendleft(self.root)
        while dq:
            cur = dq.popleft()
            print(cur.value, end = ' ')
            if cur.right:
                dq.appendleft(cur.right)
            if cur.left:
                dq.appendleft(cur.left)
    def Postorder(self):
        stack = []
        result = []
        current = self.root
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.value)
            
            current = current.right
        return ' '.join(map(str, result))
    def levelOrder(self):
        dq = deque()
        dq.append(self.root)
        while dq:
            for i in range(len(dq)):
                cur = dq.popleft()
                print(cur.value, end = ' ')
                if cur.left:
                    dq.append(cur.left)
                if cur.right:
                    dq.append(cur.right)
    def height(self):
        def _height(node):
            if not node:
                return 0
            return 1 + max(_height(node.left),_height(node.right))
        return _height(self.root)
n = int(input())
A = list(map(int, input().split()))
t = Tree()
for i in A:
    t.add(i)
print(t.height())    