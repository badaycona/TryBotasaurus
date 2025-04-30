class MinHeap:
    def __init__(self):
        self.heap = []
    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root
    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent =  (index - 1) // 2
    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and 