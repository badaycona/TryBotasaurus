
class BinarySearchTree:
    class Node:
        def __init__(self, val, left = None, right = None):
            self.val = val
            self.left = left
            self.right = right
    def __init__(self):
        self.root = None

    def insert(self, val): 
        self.root = BinarySearchTree._insert(self.root, val)

    @staticmethod
    def _insert(node, val):
        if not node:
            return BinarySearchTree.Node(val)
        if node.val > val:
            node.left = BinarySearchTree._insert(node.left, val)
        elif node.val < val:
            node.right = BinarySearchTree._insert(node.right, val)

        return node
    def searchlower(self, val):
        return BinarySearchTree._searchlower(self.root, val = val)
    
    @staticmethod
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
        return BinarySearchTree._searchhigher(self.root, val = val)
    def _searchhigher(node, val):
        res = None
        while node:
            if node.val > val:
                res = node.val
                node = node.left
            else:
                node = node.right
        return res if res is not None else 'NULL'
    def delete(self, val): # Thêm hàm delete cơ bản (cần cho việc cập nhật core status)
        self.root = BinarySearchTree._delete(self.root, val)

    @staticmethod
    def _delete(node, val):
        if not node:
            return None
        if val < node.val:
            node.left = BinarySearchTree._delete(node.left, val)
        elif val > node.val:
            node.right = BinarySearchTree._delete(node.right, val)
        else: # node.val == val, node to be deleted
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else: # Node with two children
                # Get the inorder successor (smallest in the right subtree)
                temp_node = node.right
                while temp_node.left:
                    temp_node = temp_node.left
                node.val = temp_node.val # Copy the inorder successor's content to this node
                node.right = BinarySearchTree._delete(node.right, temp_node.val) # Delete the inorder successor
        return node


def debug():
    import sys
    line = list(sys.stdin.read().strip().split())
    tree = BinarySearchTree()
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
if __name__ == '__main__':
    debug()