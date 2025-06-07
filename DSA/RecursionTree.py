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
        def traverse(node):
            if not node:
                return
            traverse(node.left)
            print(node.value, end = ' ')
            traverse(node.right)
        traverse(self.root)
n = int(input())
A = list(map(int, input().split()))
t = Tree()
for i in A:
    t.add(i)
t.Preorder()