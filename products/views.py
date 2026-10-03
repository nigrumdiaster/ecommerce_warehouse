from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from .models import Product, Category
from .trie import ProductTrie


# =========================================================
# QUICK SORT
# =========================================================

def quick_sort_products(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    # Sắp xếp mới nhất -> cũ nhất
    left = [x for x in arr if x.created_at > pivot.created_at]

    middle = [
        x for x in arr
        if x.created_at == pivot.created_at
    ]

    right = [
        x for x in arr
        if x.created_at < pivot.created_at
    ]

    return (
        quick_sort_products(left)
        + middle
        + quick_sort_products(right)
    )


# =========================================================
# DANH SÁCH SẢN PHẨM
# =========================================================

def product_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')

    # Lấy danh sách sản phẩm
    products = Product.objects.select_related('category').all()

    # Tìm kiếm theo từ khóa
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    # Lọc theo danh mục
    if category_id:
        products = products.filter(
            category_id=category_id
        )

    # Lọc theo trạng thái
    if status_filter == 'active':
        products = products.filter(
            is_active=True
        )

    elif status_filter == 'inactive':
        products = products.filter(
            is_active=False
        )

    # Các trường được phép sắp xếp
    allowed_sort_fields = [
        'price',
        '-price',
        'name',
        '-name',
        'created_at',
        '-created_at'
    ]

    if sort_by in allowed_sort_fields:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')

    # Lấy danh mục
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

    return render(
        request,
        'products/product_list.html',
        context
    )


# =========================================================
# DASHBOARD - 10 SẢN PHẨM MỚI NHẤT
# =========================================================

def recent_dashboard_view(request):
    # Lấy tất cả sản phẩm
    all_products = list(Product.objects.all())

    # Sắp xếp bằng Quick Sort
    sorted_products = quick_sort_products(all_products)

    # Lấy 10 sản phẩm mới nhất
    recent_items = sorted_products[:10]

    return render(
        request,
        'products/recent_list.html',
        {
            'recent_items': recent_items
        }
    )


# =========================================================
# CHI TIẾT SẢN PHẨM
# =========================================================

def product_detail_mock(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )


# =========================================================
# TRIE AUTOCOMPLETE
# =========================================================

# Khởi tạo cây Trie trong bộ nhớ RAM
search_trie = ProductTrie()

is_loaded = False


def build_search_tree():
    global is_loaded

    # Chỉ đưa sản phẩm đang active vào Trie
    products = Product.objects.filter(
        is_active=True
    ).values(
        'id',
        'name'
    )

    for product in products:
        search_trie.insert(
            product['name'],
            product['id']
        )

    is_loaded = True


def autocomplete_view(request):
    global is_loaded

    # Nếu Trie chưa được tạo thì xây dựng Trie
    if not is_loaded:
        build_search_tree()

    q = request.GET.get('q', '').strip()

    # Không có từ khóa
    if not q:
        return JsonResponse(
            [],
            safe=False
        )

    # Tìm kiếm trong Trie
    suggestions = search_trie.autocomplete(
        q,
        limit=5
    )

    return JsonResponse(
        suggestions,
        safe=False
    )