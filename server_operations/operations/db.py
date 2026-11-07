import sqlite3
import os
from pathlib import Path

def get_db_connection():
    """Создает соединение с базой данных SQLite"""
    db_path = Path(__file__).parent.parent / 'data' / 'operations.db'
    return sqlite3.connect(db_path)

def execute_query(query, params=None):
    """Выполняет SQL-запрос с параметрами и возвращает результат"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Если это SELECT запрос, возвращаем результаты
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def create_tables():
    """Создает таблицы в базе данных"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Создание таблицы стоек
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS racks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            rack_kind TEXT NOT NULL
        )
        ''')
        
        # Создание таблицы операций
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            op_type TEXT NOT NULL,
            start_date DATETIME NOT NULL,
            duration INTEGER NOT NULL,
            nodes INTEGER NOT NULL,
            status TEXT NOT NULL,
            rack_id INTEGER,
            FOREIGN KEY (rack_id) REFERENCES racks (id)
        )
        ''')
        
        conn.commit()
        print("Таблицы успешно созданы")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        cursor.close()
        conn.close()

def populate_database():
    """Заполняет базу данных тестовыми данными"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Вставка стоек
        racks = [
            ('Стойка A4', 42, 'серверная'),
            ('Стойка B2', 24, 'сетевая'),
            ('Стойка C1', 36, 'хранение'),
            ('Стойка D3', 48, 'серверная'),
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO racks (name, capacity, rack_kind) VALUES (?, ?, ?)',
            racks
        )
        
        # Вставка операций
        operations = [
            ('Замена диска', 'disk-replacement', 'ремонт', '2026-10-15 09:00', 120, 2, 'выполнена', 1),
            ('Апгрейд памяти', 'memory-upgrade', 'апгрейд', '2026-10-16 10:30', 90, 1, 'выполнена', 1),
            ('Диагностика сети', 'network-diagnostics', 'диагностика', '2026-10-17 14:00', 180, 4, 'выполняется', 2),
            ('Замена вентиляторов', 'fans-replacement', 'ремонт', '2026-10-18 11:00', 60, 3, 'запланирована', 3),
            ('Установка системы', 'system-installation', 'апгрейд', '2026-10-19 08:00', 240, 1, 'запланирована', 4),
            ('Тестирование ПО', 'software-testing', 'диагностика', '2026-10-20 13:30', 150, 2, 'выполнена', 1),
            ('Модернизация хранилища', 'storage-upgrade', 'апгрейд', '2026-10-21 10:00', 300, 5, 'выполняется', 3),
            ('Обслуживание коммутатора', 'switch-maintenance', 'ремонт', '2026-10-22 15:00', 120, 1, 'запланирована', 2),
        ]
        
        cursor.executemany(
            '''INSERT OR IGNORE INTO operations 
            (title, slug, op_type, start_date, duration, nodes, status, rack_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            operations
        )
        
        conn.commit()
        print("База данных успешно заполнена тестовыми данными")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

def get_all_operations(limit=None, order_by='start_date', order_direction='DESC', min_nodes=None):
    """Получает все операции с возможностью фильтрации, сортировки и ограничения"""
    query = '''
    SELECT o.*, r.name as rack_name, r.capacity, r.rack_kind
    FROM operations o
    LEFT JOIN racks r ON o.rack_id = r.id
    '''
    
    params = []
    where_clauses = []
    
    if min_nodes is not None:
        where_clauses.append('o.nodes >= ?')
        params.append(min_nodes)
    
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    
    query += f' ORDER BY o.{order_by} {order_direction}'
    
    if limit:
        query += ' LIMIT ?'
        params.append(limit)
    
    return execute_query(query, params)

def get_operation_by_slug(slug):
    """Получает операцию по slug"""
    query = '''
    SELECT o.*, r.name as rack_name, r.capacity, r.rack_kind
    FROM operations o
    LEFT JOIN racks r ON o.rack_id = r.id
    WHERE o.slug = ?
    '''
    result = execute_query(query, (slug,))
    return result[0] if result else None

def get_all_racks():
    """Получает все стойки"""
    query = 'SELECT * FROM racks ORDER BY name'
    return execute_query(query)

def get_racks_with_operations_count():
    """Получает стойки с количеством операций"""
    query = '''
    SELECT r.*, COUNT(o.id) as operations_count
    FROM racks r
    LEFT JOIN operations o ON r.id = o.rack_id
    GROUP BY r.id
    ORDER BY r.name
    '''
    return execute_query(query)

def get_operations_statistics():
    """Получает статистику по операциям"""
    query = '''
    SELECT 
        op_type,
        COUNT(*) as count,
        AVG(duration) as avg_duration,
        SUM(nodes) as total_nodes,
        SUM(CASE WHEN status = 'выполнена' THEN 1 ELSE 0 END) as completed_count
    FROM operations
    GROUP BY op_type
    HAVING COUNT(*) > 0
    ORDER BY count DESC
    '''
    return execute_query(query)

def get_total_operations_count():
    """Получает общее количество операций"""
    query = 'SELECT COUNT(*) FROM operations'
    result = execute_query(query)
    return result[0][0] if result else 0