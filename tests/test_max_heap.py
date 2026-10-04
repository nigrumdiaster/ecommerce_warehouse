import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.datastructures.max_heap import MaxHeap


def test_push_and_peek():
    heap = MaxHeap()
    heap.push(10)
    heap.push(30)
    heap.push(20)

    # Phần tử lớn nhất phải ở đỉnh heap
    assert heap.peek() == 30
    assert len(heap) == 3


def test_pop_max():
    heap = MaxHeap()
    for val in [15, 50, 25, 40, 10]:
        heap.push(val)

    # Lấy lần lượt ra phải theo thứ tự giảm dần
    assert heap.pop_max() == 50
    assert heap.pop_max() == 40
    assert heap.pop_max() == 25
    assert heap.pop_max() == 15
    assert heap.pop_max() == 10
    assert heap.is_empty() is True


def test_build_heap():
    items = [5, 3, 17, 10, 84, 19, 6, 22, 9]
    heap = MaxHeap()
    heap.build_heap(items)

    assert heap.peek() == 84
    assert heap.pop_max() == 84
    assert heap.pop_max() == 22


def test_empty_heap():
    heap = MaxHeap()
    assert heap.is_empty() is True
    assert heap.peek() is None
    assert heap.pop_max() is None


def test_custom_key_func():
    # Giả lập đơn hàng với độ ưu tiên
    orders = [
        {"id": 1, "priority": 1, "name": "Đơn thường"},
        {"id": 2, "priority": 3, "name": "Đơn hỏa tốc"},
        {"id": 3, "priority": 2, "name": "Đơn nhanh"},
    ]

    heap = MaxHeap(key_func=lambda item: item["priority"])
    for order in orders:
        heap.push(order)

    # Đơn hỏa tốc (priority = 3) phải ra đầu tiên
    first = heap.pop_max()
    assert first["id"] == 2
    assert first["priority"] == 3

    # Đơn nhanh (priority = 2) ra tiếp theo
    second = heap.pop_max()
    assert second["id"] == 3


if __name__ == "__main__":
    test_push_and_peek()
    test_pop_max()
    test_build_heap()
    test_empty_heap()
    test_custom_key_func()
    print("[OK] All MaxHeap tests passed successfully!")
