from django.shortcuts import render
from operations.db import get_total_operations_count

def home(request):
    """Главная страница приложения"""
    total_operations = get_total_operations_count()
    
    context = {
        'title': 'Система обслуживания серверов',
        'description': 'Приложение для управления операциями технического обслуживания серверного оборудования',
        'total_operations': total_operations,
    }
    
    return render(request, 'homepage/home.html', context)