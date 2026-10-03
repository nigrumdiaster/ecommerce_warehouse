class HashTable:
    def __init__(self, size=1000):
        self.size = size
        self.count = 0  # Theo dõi số lượng phần tử thực tế
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def _resize(self, new_size):
        """Mở rộng bảng và băm lại trực tiếp các phần tử mà không cần kiểm tra trùng lặp"""
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]

        for bucket in old_table:
            for key, value in bucket:
                new_index = self._hash(key)
                self.table[new_index].append([key, value])

    def put(self, key, value):
        index = self._hash(key)

        # 1. Nếu key đã có, cập nhật giá trị (không tăng count, không cần resize)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return

        # 2. Nếu key chưa có, thêm mới
        self.table[index].append([key, value])
        self.count += 1

        # 3. Tự động mở rộng khi thêm phần tử mới khiến Load Factor >= 0.75
        if self.count / self.size >= 0.75:
            self._resize(self.size * 2)

    def get(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item[0] == key:
                return item[1]

        return None

    def delete(self, key):
        index = self._hash(key)

        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                self.count -= 1
                return True

        return False

    def __len__(self):
        return self.count

    def __contains__(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return True
        return False