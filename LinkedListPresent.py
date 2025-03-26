# import typing as tp
# class node:
#     def __init__(self):
#         self.data = data
#         self.next = None
# class linked_list:
#     def __init__(self, ctn: tp.Optional[list] = None):
#         self.head = None
#         self.tail = None
    
#         if ctn is not None:
#             for i in ctn:
#                 self.append(i)
#     def append(self, data):
#         if self.head is None:
#             self.head = node(data)
#             self.tail = self.head
#         else:
#             self.tail.next = node(data)
#             self.tail = self.tail.next

class Node:
    def __init__(self, task : str, next):
        self.task = task
        self.next = next
class TaskLinkedList:
    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail
    def add_task(self, task):
        if not self.head:
            self.head = Node(task)
            self.tail = Node(task)
        else:
            self.tail.next = Node(task)
            self.tail = self.tail.next
    def display_task(self):
        dummy = self.head
        print('[', end ='')
        while dummy:
            print(dummy.task, end = ' ')
    def remove_task(self, task):
        dummy = self.head
        while dummy:
            if dummy.next.task == task:
                dummy.next = dummy.next.next
                break
        if task == self.tail.task:
            self.tail = dummy
    