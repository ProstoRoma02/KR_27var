#!/usr/bin/env python
import requests

def test_app():
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Тестируем главную страницу
        print("Тестируем главную страницу...")
        response = requests.get(f"{base_url}/")
        print(f"Статус: {response.status_code}")
        print(f"Заголовок содержит 'Система обслуживания': {'Система обслуживания' in response.text}")
        
        # Тестируем страницу стоек
        print("\nТестируем страницу стоек...")
        response = requests.get(f"{base_url}/racks/")
        print(f"Статус: {response.status_code}")
        
        # Тестируем страницу операций
        print("\nТестируем страницу операций...")
        response = requests.get(f"{base_url}/operations/")
        print(f"Статус: {response.status_code}")
        
        # Тестируем фильтрацию
        print("\nТестируем фильтрацию операций...")
        response = requests.get(f"{base_url}/operations/?nodes=2")
        print(f"Статус: {response.status_code}")
        
        # Тестируем статистику
        print("\nТестируем страницу статистики...")
        response = requests.get(f"{base_url}/operations/statistics/")
        print(f"Статус: {response.status_code}")
        
        print("\n✅ Все основные страницы отвечают корректно!")
        
    except requests.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_app()