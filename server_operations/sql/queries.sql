-- SQL запросы для приложения "Обслуживание серверов"

-- 1. Получение всех операций с информацией о стойках
SELECT 
    o.id,
    o.title,
    o.slug,
    o.op_type,
    o.start_date,
    o.duration,
    o.nodes,
    o.status,
    r.name as rack_name,
    r.capacity,
    r.rack_kind
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
ORDER BY o.start_date DESC;

-- 2. Получение операций с фильтрацией по количеству узлов (параметризованный запрос)
SELECT 
    o.*,
    r.name as rack_name,
    r.capacity,
    r.rack_kind
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
WHERE o.nodes >= ?
ORDER BY o.start_date DESC;

-- 3. Получение операций с сортировкой и ограничением
SELECT 
    o.*,
    r.name as rack_name,
    r.capacity,
    r.rack_kind
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
ORDER BY o.duration DESC
LIMIT 5;

-- 4. Получение операции по slug
SELECT 
    o.*,
    r.name as rack_name,
    r.capacity,
    r.rack_kind
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
WHERE o.slug = ?;

-- 5. Получение всех стоек
SELECT * FROM racks ORDER BY name;

-- 6. Подсчет общего количества операций
SELECT COUNT(*) FROM operations;

-- 7. Статистика по типам операций с использованием GROUP BY и HAVING
SELECT 
    op_type,
    COUNT(*) as operation_count,
    AVG(duration) as avg_duration,
    SUM(nodes) as total_nodes
FROM operations
GROUP BY op_type
HAVING COUNT(*) > 0
ORDER BY operation_count DESC;

-- 8. Статистика по статусам операций
SELECT 
    status,
    COUNT(*) as count,
    AVG(duration) as avg_duration
FROM operations
GROUP BY status
ORDER BY count DESC;

-- 9. Получение операций по статусу
SELECT 
    o.*,
    r.name as rack_name
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
WHERE o.status = ?
ORDER BY o.start_date;

-- 10. Получение стойки с количеством операций
SELECT 
    r.*,
    COUNT(o.id) as operations_count
FROM racks r
LEFT JOIN operations o ON r.id = o.rack_id
GROUP BY r.id
ORDER BY r.name;

-- 11. Получение последних операций с ограничением
SELECT 
    o.*,
    r.name as rack_name
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
ORDER BY o.start_date DESC
LIMIT 10;

-- 12. Поиск операций по типу работы
SELECT 
    o.*,
    r.name as rack_name
FROM operations o
LEFT JOIN racks r ON o.rack_id = r.id
WHERE o.op_type = ?
ORDER BY o.start_date DESC;