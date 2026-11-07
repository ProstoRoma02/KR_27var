from django.shortcuts import render
from operations.db import get_all_racks, get_racks_with_operations_count

def rack_list(request):
    """Страница списка стоек"""
    racks = get_all_racks()
    
    # Вычисляем общую вместимость
    total_capacity = sum(rack[2] for rack in racks) if racks else 0
    
    context = {
        'title': 'Стойки серверного оборудования',
        'racks': racks,
        'total_capacity': total_capacity,
    }
    
    return render(request, 'racks/rack_list.html', context)