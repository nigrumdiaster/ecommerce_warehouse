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
    from django.shortcuts import render
from .models import Product, ProductViewHistory

def recent_dashboard_view(request):
    #1 lấy 10 sản phẩm mới tạo gần nhất
    recent_products = Product.objects.order_by('-created_at')[:10]
    
    # 2 lấy 10 sản phẩm vừa xem gần nhất
    if request.user.is_authenticated:
        # Nếu người dùng đã đăng nhập
        recent_views = ProductViewHistory.objects.filter(user=request.user).order_by('-viewed_at')[:10]
    else:
        # Nếu là khách chưa đăng nhập
        if not request.session.session_key:
            request.session.save()
        recent_views = ProductViewHistory.objects.filter(session_key=request.session.session_key).order_by('-viewed_at')[:10]
        
    context = {
        'recent_products': recent_products,
        'recent_views': recent_views,
    }
    return render(request, 'products/recent_list.html', context)
    from django.shortcuts import get_object_or_404, redirect

def product_detail_mock(request, product_id):
    # 1 tìm sản phẩm bạn vừa click vào
    product = get_object_or_404(Product, id=product_id)
    
    # 2 lưu tên sản phẩm đó vào bảng lịch sử "vừa xem"
    if request.user.is_authenticated:
        ProductViewHistory.objects.create(user=request.user, product=product)
    else:
        if not request.session.session_key:
            request.session.save()
        ProductViewHistory.objects.create(session_key=request.session.session_key, product=product)
        
    # 3chuyển hướng quay lại trang bảng điều khiển để thấy kết quả
    return redirect('recent_dashboard')