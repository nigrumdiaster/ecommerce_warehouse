from datetime import datetime
from engine.datastructures.max_heap import MaxHeap
from .models import Order, OrderProcessingLog


class OrderQueueService:
    """
    MC2
    - Sử dụng MaxHeap để quản lý các đơn hàng PENDING.
    - Khóa so sánh ưu tiên 3 cấp: (priority, -created_at, -id)
    """

    def __init__(self):
        self.heap = MaxHeap(
            key_func=lambda o: (
                o.priority,
                -o.created_at.timestamp() if o.created_at else 0,
                -o.id if o.id else 0
            )
        )
        self.loaded = False

    def load_pending_orders(self, force_reload=False):
        if self.loaded and not force_reload:
            return

        pending_orders = list(Order.objects.filter(status=Order.OrderStatus.PENDING))
        self.heap.build_heap(pending_orders)
        self.loaded = True

    def enqueue_order(self, order):
        if not self.loaded:
            self.load_pending_orders()

        if order.status == Order.OrderStatus.PENDING:
            self.heap.push(order)

    def peek_next_order(self):
        """
        Xem đơn hàng ưu tiên cao nhất tiếp theo mà không lấy ra - O(1)
        """
        if not self.loaded:
            self.load_pending_orders()
        return self.heap.peek()

    def process_next_order(self, performed_by=None):
        """
        Lấy đơn hàng có độ ưu tiên cao nhất ra khỏi hàng đợi để xử lý - O(log N):
        """
        if not self.loaded:
            self.load_pending_orders()

        order = self.heap.pop_max()
        if not order:
            return None

        # Cập nhật trạng thái trong Database
        order.status = Order.OrderStatus.PROCESSING
        if performed_by and performed_by.is_authenticated:
            order.processed_by = performed_by
        order.save(update_fields=['status', 'processed_by', 'updated_at'])

        # Ghi log lịch sử
        OrderProcessingLog.objects.create(
            order=order,
            action=f"Bắt đầu đóng gói / Xử lý kho (Mức ưu tiên: {order.get_priority_display()})",
            performed_by=performed_by if (performed_by and performed_by.is_authenticated) else None
        )

        return order

    def get_queue_list(self):
        """
        Lấy danh sách các đơn hàng trong hàng đợi để hiển thị lên Dashboard.
        """
        if not self.loaded:
            self.load_pending_orders()
        return list(self.heap.heap)

    def size(self):
        """Số lượng đơn hàng đang chờ trong hàng đợi"""
        if not self.loaded:
            self.load_pending_orders()
        return len(self.heap)



order_queue_service = OrderQueueService()
