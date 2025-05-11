import random

class TreapNode:
    __slots__ = ('value', 'priority', 'left', 'right', 'size')
    def __init__(self, value):
        self.value = value
        self.priority = random.random()
        self.left = None
        self.right = None
        self.size = 1


def update_size(node):
    if node:
        node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)


def split(root, k):
    """
    Split treap into (L, R) where L contains first k elements (0..k-1), R contains rest.
    """
    if not root:
        return None, None
    left_size = root.left.size if root.left else 0
    if k <= left_size:
        # entire split in left subtree
        L, root.left = split(root.left, k)
        update_size(root)
        return L, root
    else:
        # split in right subtree
        root.right, R = split(root.right, k - left_size - 1)
        update_size(root)
        return root, R


def merge(left, right):
    """Merge two treaps where all keys in left come before keys in right"""
    if not left or not right:
        return left or right
    if left.priority > right.priority:
        left.right = merge(left.right, right)
        update_size(left)
        return left
    else:
        right.left = merge(left, right.left)
        update_size(right)
        return right


def build_treap_from_sequence(seq):
    """Builds a treap containing seq in-order"""
    root = None
    for idx, v in enumerate(seq):
        node = TreapNode(v)
        root = insert(root, node, idx)
    return root


def insert(root, node, idx):
    """Insert node at position idx in-order"""
    L, R = split(root, idx)
    return merge(merge(L, node), R)


def inorder(root, out=None):
    if out is None:
        out = []
    if not root:
        return out
    inorder(root.left, out)
    out.append(root.value)
    inorder(root.right, out)
    return out

class EulerTourTree:
    def __init__(self, seq):
        # initial euler tour sequence
        self.root = build_treap_from_sequence(seq)

    def link(self, other, u, v):
        """
        Link this tree and `other` tree by edge (u,v).
        splicing their Euler tours with two new back-and-forth visits.
        """
        # find first occurrence indices
        seq1 = inorder(self.root)
        seq2 = inorder(other.root)
        i = seq1.index(u)
        j = seq2.index(v)
        # split at i+1 and j+1
        A, B = split(self.root, i+1)
        C, D = split(other.root, j+1)
        # create the two cross visits
        node_v = TreapNode(v)
        node_u = TreapNode(u)
        # merge: A + v + C + u + D + B
        mid = merge(merge(node_v, C), node_u)
        self.root = merge(merge(A, mid), merge(D, B))

    def cut(self, u, v):
        """
        Cut the edge (u,v) from the tour by removing the two cross visits.
        """
        # get sequence and indices of cross visits
        seq = inorder(self.root)
        # find two positions of visits between u and v
        # occurrences where sequence[idx]==v next seq[idx+1]==..., naive removal
        # for simplicity, rebuild naive
        # remove first u->v and first v->u patterns
        import itertools
        new_seq = []
        it = iter(range(len(seq)-1))
        i1=j1=None
        # find u->v
        for i in it:
            if seq[i]==u and seq[i+1]==v:
                i1=i
                break
        # find v->u after
        for j in range(i1+1, len(seq)-1):
            if seq[j]==v and seq[j+1]==u:
                j1=j
                break
        # rebuild segments
        new_seq1 = seq[:i1+1] + seq[j1+1:]
        new_seq2 = seq[i1+1:j1+1]
        # two new trees
        self.root = build_treap_from_sequence(new_seq1)
        return EulerTourTree(new_seq2)

# Example usage
if __name__ == '__main__':
    A = EulerTourTree([6,7,6])
    B = EulerTourTree([1,2,3,2,1])
    A.link(B, 7, 2)
    print(inorder(A.root))  # [6,7,2,1,2,3,2,7,6]  
