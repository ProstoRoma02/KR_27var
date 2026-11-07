from django.shortcuts import render, get_object_or_404
from django.http import Http404
from operations.db import (
    get_all_operations, 
    get_operation_by_slug, 
    get_operations_statistics,
    execute_query
)

def operation_list(request):
    """Страница списка операций с фильтрацией и сортировкой"""
    # Получаем параметры фильтрации из GET запроса
    min_nodes = request.GET.get('nodes')
    limit = request.GET.get('limit')
    order_by = request.GET.get('order_by', 'start_date')
    order_direction = request.GET.get('order_direction', 'DESC')
    
    # Преобразуем параметры
    min_nodes_int = int(min_nodes) if min_nodes and min_nodes.isdigit() else None
    limit_int = int(limit) if limit and limit.isdigit() else None
    
    # Валидация параметров сортировки
    valid_order_fields = ['start_date', 'duration', 'nodes', 'title']
    if order_by not in valid_order_fields:
        order_by = 'start_date'
    
    if order_direction not in ['ASC', 'DESC']:
        order_direction = 'DESC'
    
    # Получаем операции с фильтрацией
    operations = get_all_operations(
        limit=limit_int,
        order_by=order_by,
        order_direction=order_direction,
        min_nodes=min_nodes_int
    )
    
    # Преобразуем результат в список словарей для удобства работы в шаблоне
    operations_list = []
    for op in operations:
        operations_list.append({
            'id': op[0],
            'title': op[1],
            'slug': op[2],
            'op_type': op[3],
            'start_date': op[4],
            'duration': op[5],
            'nodes': op[6],
            'status': op[7],
            'rack_id': op[8],
            'rack_name': op[9] or 'Стойка не указана',
            'capacity': op[10],
            'rack_kind': op[11],
        })
    
    context = {
        'title': 'Список операций',
        'operations': operations_list,
        'filter_nodes': min_nodes,
        'filter_limit': limit,
        'filter_order_by': order_by,
        'filter_order_direction': order_direction,
        'total_count': len(operations_list),
    }
    
    return render(request, 'operations/operation_list.html', context)

def operation_detail(request, slug):
    """Страница детальной информации об операции"""
    try:
        operation_data = get_operation_by_slug(slug)
        
        if not operation_data:
            raise Http404("Операция не найдена")
        
        # Преобразуем результат в словарь
        operation = {
            'id': operation_data[0],
            'title': operation_data[1],
            'slug': operation_data[2],
            'op_type': operation_data[3],
            'start_date': operation_data[4],
            'duration': operation_data[5],
            'nodes': operation_data[6],
            'status': operation_data[7],
            'rack_id': operation_data[8],
            'rack_name': operation_data[9] or 'Стойка не указана',
            'capacity': operation_data[10],
            'rack_kind': operation_data[11],
        }
        
        context = {
            'title': operation['title'],
            'operation': operation,
        }
        
        return render(request, 'operations/operation_detail.html', context)
    
    except Exception as e:
        # Обработка ошибок базы данных
        context = {
            'title': 'Ошибка',
            'error_message': 'Произошла ошибка при получении данных операции',
        }
        return render(request, 'operations/error.html', context, status=500)

def statistics(request):
    """Страница статистики операций"""
    try:
        stats = get_operations_statistics()
        
        # Преобразуем результат в список словарей
        stats_list = []
        total_count = 0
        total_nodes = 0
        
        for stat in stats:
            stats_list.append({
                'op_type': stat[0],
                'count': stat[1],
                'avg_duration': round(stat[2], 1) if stat[2] else 0,
                'total_nodes': stat[3],
                'completed_count': stat[4],
            })
            total_count += stat[1]
            total_nodes += stat[3]
        
        # Вычисляем среднюю длительность по всем операциям
        avg_duration_all = 0
        if stats_list:
            total_duration = sum(stat['avg_duration'] * stat['count'] for stat in stats_list)
            avg_duration_all = round(total_duration / total_count, 1) if total_count > 0 else 0
        
        context = {
            'title': 'Статистика операций',
            'statistics': stats_list,
            'total_count': total_count,
            'total_nodes': total_nodes,
            'avg_duration': avg_duration_all,
        }
        
        return render(request, 'operations/statistics.html', context)
    
    except Exception as e:
        # Обработка ошибок базы данных
        context = {
            'title': 'Ошибка',
            'error_message': 'Произошла ошибка при получении статистики',
        }
        return render(request, 'operations/error.html', context, status=500)