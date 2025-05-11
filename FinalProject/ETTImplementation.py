from abc import ABC, abstractmethod
from typing import List
from random import random


# For cleaning folder

class DynamicForest(ABC):
    """
    Abstract base class for dynamic forest algorithms.
    """
    
    def __init__(self):
        """Initialize the dynamic forest."""
        pass
    
    @abstractmethod
    def add_node(self) -> int:
        """
        Add a new node to the forest, nothing else.
        
        Returns:
            int: The ID of the new node.
        """
        pass
    
    @abstractmethod
    def link(self, i : int, j : int) -> None:
        """
        Link two nodes in the forest.
        
        Making i the parent of j.

        Throws an exception if link i and j would create a cycle.
        """

        pass

    @abstractmethod
    def cut(self, i : int, j : int) -> None:
        """
        Cut the edge between i and j.
        
        Throws an exception if i and j are not linked.
        """
        
        pass
    
    @abstractmethod
    def root(self, i : int) -> int:
        """
        Find the root of the tree containing node i.
        """

        pass
    
    @abstractmethod
    def remove_node(self, i : int) -> None:
        """
        Remove a node from the forest.
        
        Throws an exception if degree of i is not 0 (i.e. i is not linked to any node).
        """

        pass

    @abstractmethod
    def neighbors(self, i : int) -> List[int]:
        """
        Return the list containing the neighbors of i. (i.e. the nodes linked to i).
        """
    
        pass

class ListElement:
    """ An item in the skip list."""
    def __init__(self, index : int):
        # Generate height of the node. (i.e. the number of levels of this node in the skip list)

        self.height = 0
        while random() < 0.5:
            self.height += 1

        #Initialize the previous and next pointers for each level.
        self.next_pointers = {i : None for i in range(self.height + 1)}
        self.previous_pointers = {i : None for i in range(self.height + 1)}

        self.index = index
    
    def next(self) -> 'ListElement':
        """
        Return the next node in the skip list.
        """

        return self.next_pointers[0] 
    def previous(self) -> 'ListElement':
        """
        Return the previous node in the skip list.
        """

        return self.previous_pointers[0]
    
    def head(self) -> 'ListElement':
        """
        Return the head of the skip list.

        O(log(n)) time complexity
        """

        current = self

        while True:
            for i in reversed(range(current.height + 1)):
                if current.previous_pointers[i] is not None:
                    current = current.previous_pointers[i]
                    have_previous = True
                    break
     
            #If can not find any previous node, current node shall be the head
            else:
                return current
    def tail(self) -> 'ListElement':
        """
        Return the last node in the skip list.

        O(log(n)) time complexity
        """

        current : ListElement = self

        while True: 
            not_tail = False
            for i in reversed(range(current.height + 1)):
                if current.next_pointers[i] is not None:
                    current = current.next_pointers[i] 
                    not_tail = True
                    break
            if not not_tail:
                #IF can not find any next node, current node shall be the tail
                return current
    #Using for supporting method insert_after()
    def get_max_height_backward(self) -> int:
        """
        Return the maximum height of all the previous nodes, self counted.
        
        O(log(n)) time complexity
        """

        current = self
        max_height = 0

        while current is not None:
            if current.height > max_height:
                max_height = current.height
            
            current = current.previous_pointers[current.height]
        
        return max_height
    

    #Using for supporting method insert_before()
    def get_max_height_foward(self) -> int:
        """
        Return the maximum height of all the next nodes, self counted.
        
        O(log(n)) time complexity
        """

        current = self
        max_height = 0

        while current is not None:
            if current.height > max_height:
                max_height = current.height
            
            current = current.next_pointers[current.height]
        
        return max_height
    
    #Using for supporting method insert_before()
    def link_backwards_at_height(self, h, other_list_start) -> None:
        """ Link the current node to the start of the other list at height h."""
        this_list_node = self
        #Find the nearest node backward having the same height h.
        while this_list_node is not None and this_list_node.height < h:
            this_list_node = this_list_node.previous_pointers[this_list_node.height]
        
        other_list_node = other_list_start
        
        #Find the nearest node foward having the same height h.
        while other_list_node is not None and other_list_node.height < h:
            other_list_node = other_list_node.next_pointers[other_list_node.height]

        #Link two list
        if this_list_node is not None:
            this_list_node.next_pointers[h] = other_list_node
        if other_list_node is not None:
            other_list_node.previous_pointers[h] = this_list_node
        
    #Using for supporting method insert_after()
    def link_foward_at_height(self, h, other_list_end : 'ListElement') -> None:
        """Link the end of the other list to the next node of this node in this list, at height h"""

        this_list_node = self.next()
        while this_list_node is not None and this_list_node.height < h:
            this_list_node = this_list_node.next_pointers[this_list_node.height]

        other_list_node = other_list_end
        while other_list_node is not None and other_list_node.height < h:
            other_list_node = other_list_node.previous_pointers[other_list_node.height]
        
        if this_list_node is not None:
            this_list_node.previous_pointers[h] = other_list_node
        if other_list_node is not None:
            other_list_node.next_pointers[h] = this_list_node

    def insert_after(self, other_list_start : 'ListElement', other_list_end : 'ListElement') -> None:
        """ Insert another list to this list after this node."""
        
        max_height = other_list_start.get_max_height_foward()
        self_foward_height = self.get_max_height_foward()
        self_backward_height = self.get_max_height_backward()

        for h in reversed(range(1, max_height + 1)):
            if self_backward_height >= h:
                self.link_backwards_at_height(h, other_list_start)
            if self_foward_height >= h:
                self.link_foward_at_height(h, other_list_end)
        other_list_end.next_pointers[0] = self.next_pointers[0]
        if self.next_pointers[0] is not None:
            self.next_pointers[0].previous_pointers[0] = other_list_end
        self.next_pointers[0] = other_list_start
        other_list_start.previous_pointers[0] = self
    
    def split_after(self) -> None:
        """Split and take the list from the start to this node, get rid of the remain."""

        #If this position is the end of the list, return right away
        next = self.next()
        if next is None:
            return
        
        #Unlink this node of the next of it
        current = self
        current_highest_height = -1 # Highest height of all nodes encountered
        while current is not None:
            if current.height > current_highest_height:
                for h in range(current_highest_height + 1, current.height + 1):
                    current.next_pointers[h] = None
                current_highest_height = current.height
            current = current.previous_pointers[current.height]
        
        #Unlink the next node of this of this node
        current = next
        current_highest_height = -1
        while current is not None:
            if current.height > current_highest_height:
                for h in range(current_highest_height + 1, current.height + 1):
                    current.previous_pointers[h] = None
                current_highest_height = current.height
            current = current.next_pointers[current.height]
        
class Node:
    def __init__(self, index, euler_tour_element):
        self.index = index
        self.neighbors = set()
        self.euler_tour_element = euler_tour_element

class EulerTourForest(DynamicForest):
    def __init__(self):
        """
        Initialize the tree with no node"""
        super().__init__()
        
        self.next_index = 0
        self.nodes = {}

        #Keep track of all of the edges in the forest, each in this formula {Node : Node}

        self.edges = {}

    def make_root(self, index):
        """
        Make i the root of its tree, rendering it appear to be the first and the last of the euler tour tree

        This is not really reframe the euler tour as node i being the root, just relocating the sequence a little bit for convenience 
        """

        node = self.nodes[index]
        node_element = node.euler_tour_element

        previous = node_element.previous()
        head = node_element.head()
        tail = node_element.tail()

        if previous is None:
            return
        previous.split_after()
        tail.insert_after(head, previous)

    def add_node(self) -> int:
        """
        Add node to the forest, yet, unlinked to any tree
        
        Return the index of this node
        """

        new_node_index = self.next_index
        self.next_index += 1

        euler_tour_element = ListElement(new_node_index)
        self.nodes[new_node_index] = Node(new_node_index, euler_tour_element)

        return new_node_index
    
    def root(self, index : int) -> int:
        """ Return the index of the root of tree containing this node """
        if index not in self.nodes:
            raise ValueError(f'There is no nodes {index}')
        
        return self.nodes[index].euler_tour_element.head().index
    
    def neighbors(self, index) -> List[int]:
        """ Return list of the index of all nodes linked to this node"""
        if index not in self.nodes:
            raise ValueError(f'There is no nodes {index}')
        return self.nodes[index].neighbors
    
    def remove_node(self, i) -> None:
        if len(self.nodes[i].neighbors) != 0:
            raise ValueError(f'This node still links with some other nodes')
        del self.nodes[i]
    def link(self, i : int, j : int):
        if self.root(i) == self.root(j):
            return
        
        # Work object we focus from now on
        node_i_element : ListElement = self.nodes[i].euler_tour_element
        node_j_element  : ListElement = self.nodes[j].euler_tour_element

        # Before the process, make sure to store the former edge of i
        former_edge = None
        if not (node_i_element.next() is None and node_i_element.previous() is None):
            if node_i_element.next():
                former_edge = (i, node_i_element.next().index)
            else:
                former_edge = (i, node_i_element.head().index)
        
        # Need to make j the first nodes in its list to merge
        already_root = node_j_element.previous() is None
        if not already_root:
            self.make_root(j)
        # Example list: [1 2 3 2 1]
        # Make_root(2)
        # After make_root: [2 3 2 1 1] (1 repeat 2 times as it is the former head of this list, nothing wrong here)

        # Only when node j is not isolated this condition continues
        # If not, e.g [1] we only need it being the same, not [1 1]
        # [1] [2] => [1 2 1]
        # [0 1 2 1 0] [3 4 3] link(2, 3) => [0 1 2 3 4 3 2 1 0]
        last_of_j = node_j_element.tail()
        if not already_root:
            last_of_j = ListElement(j)
            node_j_element.insert_after(last_of_j, last_of_j) #Now the example become [2 3 2 1 1 2]

        # E.g [6 7 6] link with the example above [2 3 2 1 1 2] at node 7 should be [6 7 2 3 2 1 1 2 7 6], so we need to add another 7 
        # E.g [8] link with also that very example, should be [8 2 3 2 1 1 2 8]
        
        new_tail_again = ListElement(i)
        last_of_j.insert_after(new_tail_again, new_tail_again)

        # Merge together
        tail_j = node_j_element.tail()
        node_i_element.insert_after(node_j_element, tail_j)

        #Update edges
        self.edges[(i, j)] = node_i_element
        self.edges[(j, i)] = last_of_j

        #Update neighbors
        self.nodes[i].neighbors.add(j)
        self.nodes[j].neighbors.add(i)

        #Adjust former edge
        #Look at example [6 7 6], the edge in the first place is (7 -> 6) but later that 7 is occupied by 2 so now we need to relocate the pointer to the new 7 we created earlier
        if former_edge:
            self.edges[former_edge] = new_tail_again
    
    def cut(self, i : int, j : int) -> None:

        # [1 2 3 4 3 2 1] [6] cut(2,6) return nothing
        
        # [1 2* 3* 4 3^ 2^ 1] cut(2, 3) create two subtree (1 2 1) (3 4 3)
        # locate the first 2 and first 3 (sign *) and next 2 (sign ^) and next 3 
        # split after first 2 => [1 2] [ 3 4 3 2 1]
        # split after next 3 => [1 2] [3 4 3] [2 1]
        # merge first and last list, delete next 2 => [1 2 1]

        # [2 3 4 3 2] cut (2, 3) create [2] and [3 4 3] 
        # [2] [3 4 3 2]
        # [2] [3 4 3] [2]
        # [2]

        # [2 3 2] cut(2, 3) create [2] and [3]
        # [2] [3 2]
        # [2] [3] [2]
        # [2]


        # => Always delete the next i 
        if i not in self.nodes[j].neighbors:
            raise ValueError(f'{i} is not linked with {j} in the first place')
        
        first_i : ListElement = self.edges[(i, j)]
        next_j : ListElement = self.edges[(j, i)]

        next_i : ListElement = next_j.next() 
        first_j : ListElement = first_i.next() 

        first_i.split_after()
        next_j.split_after()

        tail = next_i.tail()
        if next_i.next():
            first_i.insert_after(next_i.next(), tail)
        
        del next_i

        self.nodes[i].neighbors.remove(j)
        self.nodes[j].neighbors.remove(i)

        del self.edges[(i, j)]
        del self.edges[(j, i)]
        
        # [0 1 2 3 4 3 2 1 0]
        # cut(1, 2)
        # [0 1] [2 3 4 3 2] [1 0]
    def print_forest(self):
        """For debug only"""
        self.drawn = set()
        for n in self.nodes.values():
            if n.index not in self.drawn:
                current_elem = n.euler_tour_element.head()
                current_height = current_elem.height + 1

                while current_elem is not None:
                    this_height = current_elem.height + 1
                    current_height = max(current_height, this_height)
                    print(f"[{current_elem.index}] {''.join(['*' for _ in range(this_height)])}{''.join(['|' for _ in range(current_height - this_height)])}")
                    print(f"    {''.join(['|' for _ in range(current_height)])}")
                    self.drawn.add(current_elem.index)
                    current_elem = current_elem.next()

                print(f"[*] {''.join(['*' for _ in range(current_height)])}")
                print()


# Khởi tạo một Euler Tour Forest
forest = EulerTourForest()

# Thêm các node vào forest
print("Thêm các node vào forest:")
node_0 = forest.add_node()  # Node 0
node_1 = forest.add_node()  # Node 1
node_2 = forest.add_node()  # Node 2
node_3 = forest.add_node()  # Node 3
node_4 = forest.add_node()  # Node 4
print(f"Đã thêm các node: {node_0}, {node_1}, {node_2}, {node_3}, {node_4}")
print()

# Liên kết các node
print("Liên kết các node:")
forest.link(node_0, node_1)  # Link 0-1
forest.link(node_1, node_2)  # Link 1-2
forest.link(node_3, node_4)  # Link 3-4
print("Cây sau khi liên kết:")

# Liên kết hai cây
print("Liên kết hai cây:")
forest.link(node_2, node_3)  # Link 2-3
print("Cây sau khi liên kết hai cây:")
forest.print_forest()
print()

# Cắt một cạnh
print("Cắt cạnh giữa 1 và 2:")
forest.cut(node_1, node_2)  # Cut 1-2
print("Cây sau khi cắt cạnh:")
forest.print_forest()
print()
# [0 1 0] [2 3 4 3 2]
# Cắt một cạnh khác
print("Cắt cạnh giữa 4 và 5:")
forest.cut(node_3, node_4)  # Cut 3-4
print("Cây sau khi cắt cạnh:")
forest.print_forest()
print()

#[0 1 0] [2 3 2] [4]
