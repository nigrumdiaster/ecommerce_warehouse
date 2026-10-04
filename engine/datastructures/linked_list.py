class Node:
    """Node trong Danh sách liên kết đơn (chỉ có con trỏ next)"""
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    def __init__(self, capacity=8):
        self.head = None
        self.count = 0
        self.capacity = capacity

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.count

    def prepend(self, data):
        """Thêm phần tử vào đầu danh sách - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.count += 1
        return new_node

    def remove_by_id(self, item_id, id_getter=lambda x: getattr(x, 'id', x)):
        """Tìm và xóa node có id tương ứng - O(N)"""
        if self.head is None:
            return False

        # Nếu node cần xóa là head
        if id_getter(self.head.data) == item_id:
            self.head = self.head.next
            self.count -= 1
            return True

        # Duyệt tìm node ở giữa hoặc cuối
        prev = self.head
        current = self.head.next
        while current:
            if id_getter(current.data) == item_id:
                prev.next = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next

        return False

    def remove_tail(self):
        """Xóa phần tử cũ nhất ở cuối danh sách khi vượt quá giới hạn - O(N)"""
        if self.head is None:
            return None

        # Danh sách chỉ có 1 phần tử
        if self.head.next is None:
            data = self.head.data
            self.head = None
            self.count = 0
            return data

        # Danh sách có >= 2 phần tử: tìm phần tử kế cuối
        prev = self.head
        current = self.head.next
        while current.next:
            prev = current
            current = current.next

        data = current.data
        prev.next = None
        self.count -= 1
        return data

    def add_recently_viewed(self, item, id_getter=lambda x: getattr(x, 'id', x)):
        item_id = id_getter(item)
        self.remove_by_id(item_id, id_getter)
        self.prepend(item)

        if self.count > self.capacity:
            self.remove_tail()

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        self.head = None
        self.count = 0

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


# Alias tương thích nếu cần
SinglyLinkedList = LinkedList
SinglyNode = Node
