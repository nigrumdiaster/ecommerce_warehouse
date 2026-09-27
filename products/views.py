from django.shortcuts import render, get_object_or_404
from .models import Product
#quicksort
def quick_sort_products(arr):
    if len(arr) <= 1:
        return arr
        
    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x.created_at > pivot.created_at]
    middle = [x for x in arr if x.created_at == pivot.created_at]
    right = [x for x in arr if x.created_at < pivot.created_at]
    
    return quick_sort_products(left) + middle + quick_sort_products(right)
    #hàm hiển thị danh sách
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })
#hàm hàng vừa xem, vừa nhập kho
def recent_dashboard_view(request):
    all_products = list(Product.objects.all())
    sorted_products = quick_sort_products(all_products)
    recent_items = sorted_products[:10] 
    
    return render(request, 'products/recent_list.html', {
        'recent_items': recent_items
    })
#hàm xem chi tiết sản phẩm
def product_detail_mock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })