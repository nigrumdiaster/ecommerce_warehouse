class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        index = self._hash(key)

        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return

        self.table[index].append([key, value])

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
                return True

        return False