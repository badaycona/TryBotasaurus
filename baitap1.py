class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1
class AVLTree:
    def __init__(self):
        self.root = None
    def height(self, node):
        return node.height if node else 0
    def size(self, node):
        return node.size if node else 0
    def update(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        node.size = 1 + self.size(node.left) + self.size(node.right)
    def balance(self, node):
        return self.height(node.left) - self.height(node.right)
    def rotate_left(self, node):
        oriright = node.right
        leftofright = oriright.left

        oriright.left = node
        node.right = leftofright

        self.update(node)
        self.update(oriright)

        return oriright
    def rotate_right(self, node):
        orileft = node.left
        rightofleft = orileft.right

        orileft.right = node
        node.left = rightofleft

        self.update(node)
        self.update(orileft)

        return orileft

    def insert(self, val):
        self.root = AVLTree._insert(self.root, val)
    def _insert(node, val):
        if not node:
            return Node(val)
        if val < node.val:
            node.left = AVLTree._insert(node.left, val)
        elif val > node.val:
            node.right = AVLTree._insert(node.right, val)
        else:
            return node
        
        AVLTree.update(node)

        balance = AVLTree.balance(node)

        if balance > 1 and val < node.left.val:
            return AVLTree.rotate_right(node)
        if balance < -1 and val > node.right.val:
            return AVLTree.rotate_left(node)
        if balance > 1 and val > node.left.val:
            node.left = AVLTree.rotate_left(node.left)
            return AVLTree.rotate_right(node)
        if balance < -1 and val < node.right.val:
            node.right = AVLTree.rotate_right(node.right)
            return AVLTree.rotate_left(node)
        
        return node