from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên nhà cung cấp")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email liên hệ")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"

    def __str__(self):
        return self.name


class Stock(models.Model):
    """
    Quản lý tồn kho của từng sản phẩm
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock', verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Số lượng tồn")
    min_threshold = models.PositiveIntegerField(default=5, verbose_name="Ngưỡng cảnh báo sắp hết hàng")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    class Meta:
        verbose_name = "Tồn kho"
        verbose_name_plural = "Quản lý tồn kho"

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"


class StockReceipt(models.Model):
    """
    Phiếu nhập kho (Hỗ trợ danh sách 'Vừa nhập kho' - mô hình Stack / Queue LIFO)
    """
    class ReceiptStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Nháp'
        COMPLETED = 'COMPLETED', 'Đã nhập kho'
        CANCELLED = 'CANCELLED', 'Đã hủy'

    receipt_code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Mã phiếu nhập")
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receipts',
        verbose_name="Nhà cung cấp"
    )
    status = models.CharField(
        max_length=20,
        choices=ReceiptStatus.choices,
        default=ReceiptStatus.COMPLETED,
        verbose_name="Trạng thái"
    )
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_receipts',
        verbose_name="Nhân viên nhận"
    )
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú nhập kho")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Thời gian nhập kho")

    class Meta:
        verbose_name = "Phiếu nhập kho"
        verbose_name_plural = "Danh sách vừa nhập kho"
        ordering = ['-created_at']

    def __str__(self):
        return f"Phiếu #{self.receipt_code} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class StockReceiptItem(models.Model):
    receipt = models.ForeignKey(
        StockReceipt,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Phiếu nhập"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='receipt_items',
        verbose_name="Sản phẩm"
    )
    quantity = models.PositiveIntegerField(verbose_name="Số lượng nhập")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Giá nhập")

    class Meta:
        verbose_name = "Chi tiết nhập kho"
        verbose_name_plural = "Chi tiết nhập kho"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
