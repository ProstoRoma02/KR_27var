#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from operations.db import create_tables, populate_database

if __name__ == '__main__':
    print("Создание таблиц в базе данных...")
    create_tables()
    
    print("Заполнение базы данных тестовыми данными...")
    populate_database()
    
    print("База данных успешно инициализирована!")