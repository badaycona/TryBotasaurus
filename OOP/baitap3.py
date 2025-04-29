class Node:
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
class Tree:
    def __init__(self):
        self.root = None
    def insert(self, val):
        self.root = Tree._insert(self.root, val)
    def _insert(node, val):
        if not node:
            return Node(val)
        if node.val > val:
            node.left = Tree._insert(node.left, val)
        elif node.val < val:
            node.right = Tree._insert(node.right, val)
        return node
    def searchlower(self, val):
        return Tree._searchlower(self.root, val = val)
    def _searchlower(node, val):
        res = None
        while node:
            if val <= node.val:
                node = node.left
            else:
                res = node.val
                node = node.right
        return res if res is not None else 'NULL'
    def searchhigher(self, val):
        return Tree._searchhigher(self.root, val = val)
    def _searchhigher(node, val):
        res = None
        while node:
            if node.val > val:
                res = node.val
                node = node.left
            else:
                node = node.right
        return res if res is not None else 'NULL'
import sys
line = list(sys.stdin.read().strip().split())
tree = Tree()
kq = []
for i in range(0, len(line), 2):
    cur = line[i]
    if cur == '1':
        tree.insert(int(line[i + 1]))
    elif cur == '2':
        kq.append(tree.searchlower(int(line[i + 1])))
    elif cur == '3':
        kq.append(tree.searchhigher(int(line[i + 1])))
sys.stdout.write('\n'.join(map(str, kq)))
