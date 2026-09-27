from django.shortcuts import render
from .models import Stock

def get_low_stock_recursive(inventory_list, index=0, result=None):
    if result is None:
        result = []
    
    if index >= len(inventory_list):
        return result
        
    current_item = inventory_list[index]
    if current_item.quantity <= current_item.min_threshold:
        result.append(current_item)
        
    return get_low_stock_recursive(inventory_list, index + 1, result)

def low_stock_view(request):
    all_inventory = list(Stock.objects.all())    
    
    low_stock_items = get_low_stock_recursive(all_inventory)
    
    return render(request, 'inventory/low_stock_list.html', {
        'low_stock_items': low_stock_items
    })