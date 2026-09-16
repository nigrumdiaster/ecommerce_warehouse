from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category
from .services import product_lookup_service


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')

    # Lấy danh sách sản phẩm cơ bản từ database
    products = Product.objects.select_related('category').all()

    # Tìm kiếm theo từ khóa nếu có
    if query:
        product = product_lookup_service.lookup(query)

        if product:
            # Tìm thấy chính xác SKU trong HashTable (RAM) -> Trả về ngay, không query database
            return render(request, 'products/product_list.html', {
                'products': [product],
                'categories': Category.objects.all(),
                'query': query,
                'selected_category': category_id,
                'selected_status': status_filter,
                'selected_sort': sort_by,
                'total_count': 1,
            })
        else:
            # Không khớp SKU -> Tìm kiếm Database theo tên và mô tả
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    # Lọc theo danh mục (Category)
    if category_id:
        products = products.filter(category_id=category_id)

    # Lọc trạng thái (Active / Inactive)
    if status_filter == 'active':
        products = products.filter(is_active=True)
    elif status_filter == 'inactive':
        products = products.filter(is_active=False)

    # Sắp xếp
    allowed_sort_fields = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
    if sort_by in allowed_sort_fields:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_status': status_filter,
        'selected_sort': sort_by,
        'total_count': products.count(),
    }
    return render(request, 'products/product_list.html', context)

