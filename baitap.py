class Node:
    _slots_ = ['val', 'left', 'right', 'size']
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
        self.size = 1
class Tree:
    def __init__(self):
        self.root = None
    def insert(self, val):
        self.root = Tree._insert(self.root, val)
    @staticmethod
    def _insert(node, val):
        if not node:
            node = Node(val)
            return node
        if node.val > val:
            node.left = Tree._insert(node.left, val)
        elif node.val < val:
            node.right = Tree._insert(node.right, val)
        ls = node.left.size if node.left else 0
        rs = node.right.size if node.right else 0
        node.size = 1 + ls + rs
        return node
    # def pop(self, val):
    #     self.root = Tree._pop(self.root, val)
    # def _pop(node, val):
    #     if not node:
    #         return 
    #     if node.left.val == val:
    #         node.left = None
    #         node.size -= 1
    #     elif node.right.val == val:
    #         node.right = None
    # #         node.size -= 1
    #     elif val < node.val:
    #         node.left = Tree._pop(node.left, val)
    @staticmethod
    def __rank(node, val):
        
        r = node
        rank = 1
        while r:
            left_size = r.left.size if r.left else 0
            if val == r.val:
                rank += left_size
                return rank
            elif val < r.val:
                r = r.left
            else:
                r = r.right
                rank += 1 + left_size
        return 0 
    def rank(self, val):
        return Tree.__rank(self.root, val)
        
import sys
def main():
    tree = Tree()
    for i in sys.stdin.read().strip().split('\n'):
        i = i.split()
        if len(i) == 2:
            op, val = i[0], int(i[1])
            if op == '1':
                tree.insert(val)
            else:
                print(tree.rank(val))

if __name__ == "__main__":
    main()