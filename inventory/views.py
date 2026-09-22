from django.shortcuts import render
from django.db.models import F
from .models import Stock

def low_stock_view(request):
    low_stock_items = Stock.objects.filter(quantity__lte=F('min_threshold')).select_related('product')
    
    context = {
        'low_stock_items': low_stock_items,
        'total_warnings': low_stock_items.count()
    }
    return render(request, 'inventory/low_stock_list.html', context)