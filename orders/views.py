import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderProcessingLog
from .services import order_queue_service


def order_queue_view(request):
    """
    Giao diện điều phối hàng đợi đơn hàng ưu tiên (MC2).
    """
    # Đảm bảo nạp dữ liệu vào Heap
    order_queue_service.load_pending_orders()

    next_order = order_queue_service.peek_next_order()
    queue_orders = order_queue_service.get_queue_list()
    recent_processed = Order.objects.filter(
        status__in=[Order.OrderStatus.PROCESSING, Order.OrderStatus.SHIPPED, Order.OrderStatus.DELIVERED]
    ).order_by('-updated_at')[:5]

    context = {
        'next_order': next_order,
        'queue_orders': queue_orders,
        'queue_count': len(queue_orders),
        'recent_processed': recent_processed,
    }
    return render(request, 'orders/order_queue.html', context)


def process_next_order_view(request):
    """
    Xử lý lấy đơn hàng ưu tiên cao nhất tiếp theo ra khỏi MaxHeap.
    """
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        order = order_queue_service.process_next_order(performed_by=user)

        if order:
            messages.success(
                request,
                f" Đã bốc đơn hàng #{order.order_code} ({order.get_priority_display()}) của khách hàng {order.customer_name} để xử lý kho!"
            )
        else:
            messages.warning(request, "Hàng đợi đang trống, không có đơn hàng nào cần xử lý.")

    return redirect('order_queue')


def create_mock_order_view(request):
    """
    Tạo nhanh đơn hàng mẫu để kiểm thử điều phối MaxHeap.
    """
    if request.method == 'POST':
        priority = int(request.POST.get('priority', Order.PriorityLevel.NORMAL))
        customer_name = request.POST.get('customer_name', 'Khách hàng thử nghiệm').strip()
        shipping_address = request.POST.get('shipping_address', 'TP. Hồ Chí Minh').strip()
        total_amount = float(request.POST.get('total_amount', 1500000))

        order_code = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        is_urgent = (priority == Order.PriorityLevel.URGENT)

        new_order = Order.objects.create(
            order_code=order_code,
            customer_name=customer_name or 'Khách hàng thử nghiệm',
            customer_phone='0987654321',
            shipping_address=shipping_address or 'TP. Hồ Chí Minh',
            priority=priority,
            is_urgent=is_urgent,
            status=Order.OrderStatus.PENDING,
            total_amount=total_amount,
            note="Đơn hàng tạo từ Dashboard kiểm thử"
        )

        # Đẩy đơn hàng vào MaxHeap
        order_queue_service.enqueue_order(new_order)

        messages.success(
            request,
            f" Đã tạo thành công đơn #{new_order.order_code} [{new_order.get_priority_display()}] và đẩy vào MaxHeap!"
        )

    return redirect('order_queue')


def reload_queue_view(request):
    """
    Nạp lại toàn bộ đơn PENDING từ Database vào RAM MaxHeap.
    """
    order_queue_service.load_pending_orders(force_reload=True)
    messages.info(request, " Đã đồng bộ lại hàng đợi MaxHeap từ Database!")
    return redirect('order_queue')
