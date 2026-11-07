#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import os

# Создаем простое изображение для логотипа
img = Image.new('RGB', (50, 50), color='#2c3e50')
draw = ImageDraw.Draw(img)

# Рисуем простую иконку сервера
draw.rectangle([10, 10, 40, 40], outline='#3498db', width=2)
draw.rectangle([15, 15, 35, 25], fill='#3498db')
draw.rectangle([20, 30, 30, 35], fill='#e74c3c')

# Сохраняем изображение
logo_path = os.path.join('static', 'img', 'logo.png')
img.save(logo_path)

print(f"Логотип создан: {logo_path}")
print("Размер: 50x50 пикселей")