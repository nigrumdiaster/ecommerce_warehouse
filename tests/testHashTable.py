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


def test_dynamic_resize():
    ht = HashTable(size=4)
    ht.put("k1", 1)
    ht.put("k2", 2)
    assert ht.size == 4

    # Thêm phần tử thứ 3 (3/4 = 0.75 >= 0.75) -> kích hoạt resize lên 8
    ht.put("k3", 3)
    assert ht.size == 8
    assert ht.count == 3
    assert ht.get("k1") == 1
    assert ht.get("k2") == 2
    assert ht.get("k3") == 3


def test_overwrite_does_not_resize():
    ht = HashTable(size=4)
    ht.put("k1", 1)
    ht.put("k2", 2)
    # Cập nhật giá trị cho key cũ (không tăng count, không resize)
    ht.put("k2", 200)
    assert ht.size == 4
    assert ht.count == 2
    assert ht.get("k2") == 200


def test_len_and_contains():
    ht = HashTable(size=10)
    assert len(ht) == 0

    ht.put("SP001", "iPhone")
    ht.put("SP002", None)  # Test trường hợp giá trị là None

    assert len(ht) == 2
    assert "SP001" in ht
    assert "SP002" in ht  # Vẫn phải trả về True dù giá trị là None
    assert "SP999" not in ht

    ht.delete("SP001")
    assert len(ht) == 1
    assert "SP001" not in ht