from django.db.utils import OperationalError, ProgrammingError
from categories.models import Category
from products.models import Product, ProductImage


def seed_database():
    try:
        if not Category.objects.exists():

            laptops = Category.objects.create(
                name="Ноутбуки",
                slug="laptops",
                description="Ноутбуки всіх брендів",
                image = "categories/laptops.jpg"
            )

            phones = Category.objects.create(
                name="Телефони",
                slug="phones",
                description="Смартфони",
                image = "categories/phones.jpg"
            )

        if not Product.objects.exists():

            laptops = Category.objects.get(slug="laptops")
            phones = Category.objects.get(slug="phones")

            macbook = Product.objects.create(
                name="MacBook Pro",
                price=120000,
                category=laptops,
            )

            ProductImage.objects.create(
                product=macbook,
                image="images/macbook_pro.jpg",
                priority=0
            )

            iphone = Product.objects.create(
                name="iPhone 16",
                price=65000,
                category=phones,
            )

            ProductImage.objects.create(
                product=iphone,
                image="images/iphone_16.jpg",
                priority=0
            )

    except (OperationalError, ProgrammingError):
        # Таблиці ще не створені
        pass