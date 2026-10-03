class MaxHeap:
    def __init__(self, key_func=None):
        self.heap = []
        self.key_func = key_func if key_func else (lambda x: x)

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _compare(self, item_a, item_b):
        return self.key_func(item_a) > self.key_func(item_b)

    def _sift_up(self, index):
        while index > 0:
            parent_idx = self._parent(index)
            if self._compare(self.heap[index], self.heap[parent_idx]):
                self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
                index = parent_idx
            else:
                break

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < size and self._compare(self.heap[left], self.heap[largest]):
                largest = left

            if right < size and self._compare(self.heap[right], self.heap[largest]):
                largest = right

            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop_max(self):
        if self.is_empty():
            return None

        max_item = self.heap[0]
        last_item = self.heap.pop()

        if not self.is_empty():
            self.heap[0] = last_item
            self._sift_down(0)

        return max_item

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def build_heap(self, items):
        """Xây dựng Heap từ một danh sách các phần tử cho trước - O(N)"""
        self.heap = list(items)
        n = len(self.heap)
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def is_empty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)
