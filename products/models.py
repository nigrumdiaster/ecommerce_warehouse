from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=160, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Tên sản phẩm")
    sku = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Mã SKU/Barcode")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Danh mục"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Giá bán")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Giá vốn")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chi tiết")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Hình ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Đang kinh doanh")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Danh sách sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.sku}] {self.name}"


class ProductViewHistory(models.Model):
    """
    Lưu vết sản phẩm vừa xem (Hỗ trợ cấu trúc dữ liệu LRU Cache / Stack cho 'Sản phẩm vừa xem')
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='view_histories',
        verbose_name="Người dùng"
    )
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True, verbose_name="Session Key")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name="Sản phẩm"
    )
    viewed_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Thời điểm xem")

    class Meta:
        verbose_name = "Lịch sử xem sản phẩm"
        verbose_name_plural = "Danh sách vừa xem"
        ordering = ['-viewed_at']

    def __str__(self):
        user_info = self.user.username if self.user else f"Session: {self.session_key}"
        return f"{user_info} viewed {self.product.name} at {self.viewed_at}"
