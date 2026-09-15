from engine.datastructures.hash_table import HashTable


def test_put_and_get():
    ht = HashTable()

    ht.put("SP001", "iPhone 15")
    ht.put("SP002", "MacBook")

    assert ht.get("SP001") == "iPhone 15"
    assert ht.get("SP002") == "MacBook"


def test_overwrite():
    ht = HashTable()

    ht.put("SP001", "iPhone 15")
    ht.put("SP001", "iPhone 15 Pro")

    assert ht.get("SP001") == "iPhone 15 Pro"


def test_delete():
    ht = HashTable()

    ht.put("SP001", "iPhone 15")

    assert ht.delete("SP001") is True
    assert ht.get("SP001") is None


def test_delete_key_not_found():
    ht = HashTable()

    assert ht.delete("SP999") is False


def test_get_key_not_found():
    ht = HashTable()

    assert ht.get("SP999") is None


def test_collision():
    ht = HashTable(size=5)

    # Giả lập hàm băm để cả hai key cùng trỏ về một bucket index 0 (tạo tình huống đụng độ băm)
    ht._hash = lambda key: 0

    # Dùng phương thức put để kiểm tra việc lưu cả hai key vào cùng một bucket
    ht.put("SP001", "iPhone 15")
    ht.put("SP006", "MacBook")

    # Kiểm tra cả 2 phần tử đều nằm chung trong bucket 0
    assert len(ht.table[0]) == 2

    # Kiểm tra cả hai key vẫn lấy được đúng dữ liệu thông qua cơ chế duyệt bucket (chaining)
    assert ht.get("SP001") == "iPhone 15"
    assert ht.get("SP006") == "MacBook"