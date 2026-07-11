import os # Робота з файлами та папками в ОС
from django.conf import settings # Доступ до налаштувань проекту
from PIL import Image # Робота з зображеннями
import io # Робота з байтами
import uuid # Генерація унікальних ідентифікаторів
from django.core.files.base import ContentFile # Файл яки предав користувач

def compress_image(image_field, size=(800, 800), quality=85):
    img = Image.open(image_field).convert('RGB') # Якщо фото в png, конвертуємо в RGB
    img.thumbnail(size, Image.LANCZOS) # Зберігає оригінальне співвідношення сторін згідно size
    uid = str(uuid.uuid4())[:10] # Генератор назви з 10 символів
    img_name = '{}.webp'.format(uid) # Назва файлу
    img_io = io.BytesIO() # Фото буде в пам'яті
    img.save(img_io, format='WEBP', quality=quality) # Перетворюємо зображення
    img_io.seek(0) # Зміщення на початок у пам'яті
    resized_image = ContentFile(img_io.getvalue()) # Отримуємо зображення
    return resized_image, img_name # Повертаємо зображення та його назву

def save_custom_img(image, size, folder):
    resized_image, image_name = compress_image(image, size)
    # Створюємо шлях до директорії та шлях до файлу
    dir_path = os.path.join(settings.IMAGES_ROOT, folder)
    full_path = os.path.join(dir_path, image_name)
    # Створюємо папки, якщо їх ще не існує
    os.makedirs(dir_path, exist_ok=True)
    # Зберігаємо файл
    with open(full_path, "wb") as f:
        f.write(resized_image.read())
    return image_name