from abc import ABC, abstractmethod
from random import random
from typing import Optional
class DynamicForest(ABC):
    @abstractmethod
    def __init__(self):
        """ 
        Create a forest with nothing having stored yet

        This forest shall be undirected one
        """
        pass

    @abstractmethod
    def add(self):
        """Add a node into the database stored inside the forest"""
        
        pass
    
    @abstractmethod
    def remove(self):
        """Remove a node existed inside the forest"""
        pass

    @abstractmethod
    def link(self):
        """Create a edge between two nodes"""
        pass

    @abstractmethod
    def cut(self):
        """Remove a node existed connecting two nodes"""
        pass

class EulerTourForest(DynamicForest):
    __slots__ = ['nodes', 'edges', 'next_index']
    nodes : dict[int, Optional['EulerTourForest.Node']]
    edges : dict[tuple[int, int], Optional['EulerTourForest.NodeInSkipList']]
    class NodeInSkipList:
        __slots__ = ['height', 'index', 'previous', 'next']

        previous : dict[int, Optional['EulerTourForest.NodeInSkipList']]
        next : dict[int , Optional['EulerTourForest.NodeInSkipList']]
        def __init__(self, index):
            self.height = 0 # Number of layer this node has, except for the floor layer containing all nodes

            while random() > 0.5:
                self.height += 1
            
            self.index = index # Indicating this node is the reference of which in the real tree, one index can be occupied by multiple NodeInSkipList
            self.previous = {i : None for i in range(self.height + 1)}
            self.next = {i : None for i in range(self.height + 1)}
        
        def head(self) -> 'EulerTourForest.NodeInSkipList':
            """
            Return the head of this tree a.k.a the first node

            O(log(n)) time complexity
            """
            current = self
            
            while True:
                not_head = False
                if current.previous[0] is not None:
                    for h in reversed(range(current.height + 1)):
                        if current.previous[h] is not None:
                            current = current.previous[h]
                            not_head = True
                            break
                else:
                    if not not_head:
                        return current
        def tail(self) -> 'EulerTourForest.NodeInSkipList':
            """
            Return the tail of this tree a.k.a the last node
            
            O(log(n)) time complexity
            """

            current = self
            while True:
                not_tail = False
                if current.next[0] is not None:
                    for h in reversed(range(current.height + 1)):
                        if current.next[h] is not None:
                            current = current.next[h]
                            not_tail = True
                            break
                else:
                    if not not_tail:
                        return current
                    
        def max_height_beforeward(self) -> int:
            """
            <-----
            Finding the max height from head to this node 
            """
            max_height = 0
            current = self

            while current is not None:
                if current.height > max_height:
                    max_height = current.height
                current = current.previous[current.height]
            return max_height
        def max_height_afterward(self) -> int:
            """
            ----->
            Finding the max height from this node to the tail
            """

            max_height = 0
            current = self

            while current is not None:
                if current.height > max_height:
                    max_height = current.height
                current = current.next[current.height]
            return max_height
        
        @staticmethod
        def _link_this_to_start_at_height(this_node : 'EulerTourForest.NodeInSkipList', start : 'EulerTourForest.NodeInSkipList', h : int) -> None:
            """
            Helper for insert
            """
            #Look for nearest height h+ nodes from the original list and the list merged into
            node_1 = this_node
            while node_1 and node_1.height < h:
                node_1 = node_1.previous[node_1.height]
            
            node_2 = start
            while node_2 and node_2.height < h:
                node_2 = node_2.next[node_2.height]

            if node_1:
                node_1.next[h] = node_2
            if node_2:
                node_2.previous[h] = node_1
        @staticmethod
        def _link_end_to_next_of_this(this_node : 'EulerTourForest.NodeInSkipList', end : 'EulerTourForest.NodeInSkipList', h : int) -> None:
            """
            Helper for insert
            """

            #Look for nearest height h+ nodes from the original list and the list merged into
            node_1 : EulerTourForest.NodeInSkipList = this_node.next[0]
            while node_1 and node_1.height < h:
                node_1 = node_1.next[node_1.height]

            node_2 = end
            while node_2 and node_2.height < h:
                node_2 = node_2.previous[node_2.height]

            if node_1:
                node_1.previous[h] = node_2
            if node_2:
                node_2.next[h] = node_1

        def insert(self, start : 'EulerTourForest.NodeInSkipList', end : 'EulerTourForest.NodeInSkipList') -> None:
            """
            Merge another tree after this node

            How it works:
            
            link start to this node
            link end to next of this node

            in order to do that, we need to know the height of the list link into and beforeward, afterward of this node
            """
            max_height_other_list = start.max_height_afterward()
            max_height_before = self.max_height_beforeward()
            max_height_after = self.max_height_afterward()


            for h in range(1, max_height_other_list + 1):
                if max_height_before >= h:
                    EulerTourForest.NodeInSkipList._link_this_to_start_at_height(self, start, h)
                if max_height_after >= h:
                    EulerTourForest.NodeInSkipList._link_end_to_next_of_this(self, end, h)

            next = self.next[0]
            
            self.next[0] = start
            start.previous[0] = self
            end.next[0] = next
            if next:
                next.previous[0] = end

        def split_after(self) -> None:
            """
            Split this list into two parts, making this node tail of the first and next of this the head of seccond
            """
            next = self.next[0]
            if not next:
                return
            
            current = self
            current_highest_height = -1
            while current:
                if current.height > current_highest_height:
                    for h in range(current_highest_height + 1, current.height + 1):
                        current.next[h] = None
                    current_highest_height = current.height
                current = current.previous[current.height]
            
            current = next
            current_highest_height = -1
            while current:
                if current.height > current_highest_height:
                    for h in range(current_highest_height + 1, current.height + 1):
                        current.previous[h] = None
                    current_highest_height = current.height
                current = current.next[current.height]
        def print_dict(self):
            head = self.head()
            ans = []
            while head:
                ans.append(head.index)
                head = head.next[0]
            return ans
    class Node:
        def __init__(self, index : int, reference : Optional['EulerTourForest.NodeInSkipList']):
            
            self.index = index
            self.neighbors = set()
            self.reference = reference
    
    def __init__(self):
        """Create new forest with nothing stored yet"""

        self.nodes = {}
        self.edges = {}
        self.next_index = 0

    def add(self) -> int:
        """
        Add a new node
        
        Return an integer represent the index of that node
        """
        index = self.next_index
        self.next_index += 1
        self.nodes[index] = self.Node(index, self.NodeInSkipList(index))

        return index

    def remove(self, index):
        if index not in self.nodes or len(self.nodes[index].neighbors) != 0:
            raise ValueError(f'Invalid operation')
        
        del self.nodes[index]
    
    def root(self, index) -> int:
        """ Return index of the head of skip list containing this node"""
        if index not in self.nodes:
            raise ValueError('Invalid operation')
        return self.nodes[index].reference.head().index

    def tail(self, index) -> int:
        """Return index of the tail of skip list containing this node"""
        if index not in self.nodes:
            raise ValueError('Invalid operation')
        return self.nodes[index].reference.tail().index
    
    def make_root(self, index) -> None:
        """Make this node the head of its skip list"""

        # [1 2 1] make_root(2) => [2 1 2]
        # [1 2 3 2 1] make_root(2) => [2 3 2 1 2] | make_root(3) => [3 2 1 2 3] | make_root(1) => [1 2 3 2 1] 
        # [1 2 4 6 4 2 3 2 1] make_root(6) => [6 4 2 3 2 1 2 4 6]
        # if this is root already, return instantly
        # if not, locate the first ref of i
        # make tail the new ref of head:
        # [1 2 4 6 4 2 3 2 1] 1 is head and also tail, we are going to delete the first 1 so we need to make the node 1 point to another reference, in this case, the tail 1
        # [2 4 6 4 2 3 2 1] split before first i then insert after tail, and finally create new reference of i at the end
        # [2 4] [6 4 2 3 2 1] => [6 4 2 3 2 1 2 4 6]

        
        
        i = index
        node_i_ref = self.nodes[i].reference

        if node_i_ref.previous[0] is None:
            return
        
        #[6 7 6] make_root(7) => [7 6 7]
        # Need to identify if between the head and this node has some thing, if not we need to behave differently
        # [6 7 6] make_root(7) => [7 6 7]
        index_head = node_i_ref.head().index 
        node_head = self.nodes[index_head]
        
        next_of_head = node_head.reference.next[0]
        tail_of_before = None
        ref_tail = node_i_ref.tail()
        tail = node_i_ref.tail()
        node_head.reference.split_after()
        #If there is something between head and i
        if next_of_head is not node_i_ref: 
            tail_of_before = node_i_ref.previous[0]
            tail_of_before.split_after()
        
        # [6 7 6] make_root(7) => [7 6 7], edge(6, 7) => seccond 6
        # [1 2 4 6 4 2 3 2 1 7 1] make_root(2) => [2 4 6 4 2 3 2 1 7 1 2], edge(1, 2) => last 1
        # [1 2 4 6 4 2 3 2 1 7 1] make_root(4) => [4 6 4 2 3 2 1 2 4], edge(1, 2) => seccond 1
        self.edges[(index_head, next_of_head.index)] = tail
        
        node_head.reference = ref_tail

        current_tail = ref_tail
        if tail_of_before:
            ref_tail.insert(next_of_head, tail_of_before)
            current_tail = tail_of_before

        another_node_i = self.NodeInSkipList(i)
        current_tail.insert(another_node_i, another_node_i)

    def link(self, index1 : int, index2 : int) -> None:
        """
        Create a edge between two nodes

        Reconstruct the skip list
        """
        i, j = index1, index2
        #If node i and node j are in the same tree, return right away
        if self.root(i) == self.root(j):
            return
        
        node_i = self.nodes[i]
        node_j = self.nodes[j]
        ref_i = node_i.reference
        ref_j = node_j.reference

        # E.g. [6 7* 6] link(7,2) with [2 3 2 1 2] become [6 7 2 3 2 1 2 7* 6], the edge(7, 6) initial value is 7 (* signed) but later seccond 7
        # We need to keep track of this edge to tweak later
        former_edge = None
        if ref_i.next[0]:
            former_edge = (i, ref_i.next[0].index)
        if ref_j.previous[0] is not None:
            self.make_root(j)
        last_of_j = ref_j.tail()

        new_ref_i = self.NodeInSkipList(i)
        last_of_j.insert(new_ref_i, new_ref_i)

        ref_i.insert(ref_j, new_ref_i)
        
        #Update edges
        self.edges[(i, j)] = ref_i
        self.edges[(j, i)] = last_of_j
        
        #Update neighbors
        node_i.neighbors.add(j)
        node_j.neighbors.add(i)

        #Readjust edges
        if former_edge is not None:
            self.edges[former_edge] = new_ref_i

    def cut(self, index1 : int, index2 : int) -> None:
        """
        Remove the edges between two nodes

        Create two new skip list
        """
        #Need to check wether first i or first j apppearance is nearer to head (or to tail)
        i, j = index1, index2
        # Usually, i -> then j -> i but if otherwise, j -> i then i-> j 

        #If node i and node j are not connected, return instantly

        if i not in self.nodes[j].neighbors:
            return 
        
        # [7 6 7] cut(6, 7)
        # first_i = 6, next_j = first 7, next_i = 6
        # [7] [6] [7]

        #identify two edges:
        node_i = self.edges[(i, j)]
        node_j = self.edges[(j, i)] 

        another_j = node_i.next[0]
        another_i = node_j.next[0]
        
        head = node_i.head()
        tail = node_j.tail()

        node_j.split_after()
        node_i.split_after()
        
        # [7 2 9 6 9 2 7] cut(2, 9) or cut(9, 2) return the same until now
        # => [7 2] [9 6 9] [2 7]
        # cut(2, 9) => i = 2, j = 9, i come first, j come later
        # cut(9, 2) => i = 9, j = 2, i come later, i come first
        # [head .... node_i] [another_j ... node_j] [another_i ... tail] in cut(2, 9) scenerio
        # [head .... node_j] [another_i ... node_i] [another_j ... tail] in cut(9, 2) scenerio
        # for consistent, check if tail of the first skip list node_i or node_j

        if head.tail() is node_j:
            # Check if there is something after another_j to merge
            node_to_merge = another_j.next[0]
            if node_to_merge:
                another_j.split_after()
                self.edges[j, node_to_merge.index] = node_j
                del another_j
                #Merge first and last list except for the another_i that should be deleted
                node_j.insert(node_to_merge, tail)
        else:
            node_to_merge = another_i.next[0]
            if node_to_merge:
                another_i.split_after()
                self.edges[i, node_to_merge.index] = node_i
                del another_i
                node_i.insert(node_to_merge, tail)
        
        self.nodes[i].neighbors.remove(j)
        self.nodes[j].neighbors.remove(i)

        del self.edges[(i, j)]
        del self.edges[(j, i)]

    def print_forest(self):
        """For debug only"""
        self.drawn = set()
        for n in self.nodes.values():
            if n.index not in self.drawn:
                current_elem = n.reference.head()
                current_height = current_elem.height + 1

                while current_elem is not None:
                    this_height = current_elem.height + 1
                    current_height = max(current_height, this_height)
                    print(f"[{current_elem.index}] {''.join(['*' for _ in range(this_height)])}{''.join(['|' for _ in range(current_height - this_height)])}")
                    print(f"    {''.join(['|' for _ in range(current_height)])}")
                    self.drawn.add(current_elem.index)
                    current_elem = current_elem.next[0]

                print(f"[*] {''.join(['*' for _ in range(current_height)])}")
                print()
    def transfer(self, A : Optional[list]):
        """
        Transfer a list into the forest
        A is a list of index
        """
        if A is None:
            return
        for i in range(len(A)):
            self.next_index = A[i]
            self.add()
        for i in range(len(A) - 1):
            self.link(A[i], A[i + 1])  
def testcase():
    # Khởi tạo một Euler Tour Forest
    forest = EulerTourForest()

    # Thêm các node vào forest
    print("Thêm các node vào forest:")
    forest.transfer([7,6])
    forest.print_forest()
    forest.cut(6, 7)
    forest.print_forest()
    print()

if __name__ == "__main__":
    testcase()