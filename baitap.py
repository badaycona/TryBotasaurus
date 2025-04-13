class Node:
    __slots__ = ['val', 'left', 'right', 'size']
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
    # def insert(self, val):
    #     if not self.root:
    #         self.root = Node(val)
    #         return

    #     cur = self.root
    #     while True:
    #         cur.size += 1
    #         if val < cur.val:
    #             if cur.left:
    #                 cur = cur.left
    #             else:
    #                 cur.left = Node(val)
    #                 return
    #         elif val > cur.val:
    #             if cur.right:
    #                 cur = cur.right
    #             else:
    #                 cur.right = Node(val)
    #                 return
    #         else:
    #             cur.size -= 1
    #             return
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
    def pop(self, val):
        self.root = Tree._pop(self.root, val)
    @staticmethod
    def _find_min(node):
        while node.left:
            node = node.left
        return node.val
    @staticmethod
    def _pop(node, val):
        if not node:
            return None
        if val < node.val:
            node.left = Tree._pop(node.left, val)
        elif val > node.val:
            node.right = Tree._pop(node.right, val)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            replace_value = Tree._find_min(node.right)
            node.val = replace_value    
            node.right = Tree._pop(node.right, replace_value)

        ls = node.left.size if node.left else 0
        rs = node.right.size if node.right else 0
        node.size = 1 + ls + rs
        return node
    def DFS(self):
        def backtrack(node):
            if not node:
                return
            backtrack(node.left)
            print(node.val, end = ' ')
            backtrack(node.right)
        backtrack(self.root)
        print()
import sys
def main():
    tree = Tree()
    kq = []
    for i in sys.stdin:
        if i == '\n':
            continue
        i = i.split()
        if len(i) == 2:
            op, val = i[0], int(i[1])
            if op == '1':
                tree.insert(val)
            elif op == '2':
                kq.append(str(tree.rank(val)))
            elif op == '3':
                tree.pop(val)
    sys.stdout.write('\n'.join(kq))
if __name__ == "__main__":
    main()