from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    class PriorityLevel(models.IntegerChoices):
        NORMAL = 1, '1 - Tiêu chuẩn (Normal)'
        HIGH = 2, '2 - Giao nhanh (High)'
        URGENT = 3, '3 - Hỏa tốc / Đơn gấp (Urgent)'

    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Chờ xử lý'
        CONFIRMED = 'CONFIRMED', 'Đã xác nhận'
        PROCESSING = 'PROCESSING', 'Đang đóng gói / Xử lý kho'
        SHIPPED = 'SHIPPED', 'Đang vận chuyển'
        DELIVERED = 'DELIVERED', 'Đã giao hàng'
        CANCELLED = 'CANCELLED', 'Đã hủy'

    order_code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Mã đơn hàng")
    customer_name = models.CharField(max_length=150, verbose_name="Tên khách hàng")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    shipping_address = models.TextField(verbose_name="Địa chỉ nhận hàng")
    
    # Cơ chế ưu tiên xử lý đơn gấp (Phục vụ cấu trúc Priority Queue / Max Heap)
    priority = models.IntegerField(
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
        db_index=True,
        verbose_name="Mức độ ưu tiên"
    )
    is_urgent = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Đơn hỏa tốc / Đơn gấp"
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hạn chót xử lý / Giao hàng"
    )
    
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
        verbose_name="Trạng thái đơn hàng"
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tổng tiền")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú đơn hàng")
    
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_orders',
        verbose_name="Nhân viên xử lý"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Thời gian tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lúc")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý đơn hàng"
        # Mặc định sắp xếp theo ưu tiên cao nhất trước, sau đó tới thời gian tạo (FIFO trong cùng mức ưu tiên)
        ordering = ['-priority', 'created_at']

    def __str__(self):
        return f"[{self.get_priority_display()}] Đơn #{self.order_code} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Đơn hàng"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Sản phẩm"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Đơn giá")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Thành tiền")

    class Meta:
        verbose_name = "Sản phẩm trong đơn"
        verbose_name_plural = "Chi tiết sản phẩm đơn hàng"

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class OrderProcessingLog(models.Model):
    """
    Lịch sử xử lý đơn hàng của nhân viên
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name="Đơn hàng"
    )
    action = models.CharField(max_length=255, verbose_name="Hành động")
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người thực hiện"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú thêm")

    class Meta:
        verbose_name = "Nhật ký xử lý đơn"
        verbose_name_plural = "Nhật ký xử lý đơn"
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {self.order.order_code}: {self.action}"
