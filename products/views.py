from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')

    # Lấy danh sách sản phẩm cơ bản từ database
    products = Product.objects.select_related('category').all()

    # Tìm kiếm theo từ khóa nếu có
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
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

