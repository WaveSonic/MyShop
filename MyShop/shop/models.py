from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField('Назва товару', max_length=100)
    desc = models.TextField('Опис товару')
    price = models.FloatField('Ціна товару')
    the_is = models.CharField('Наявність', max_length=1)
    category = models.CharField('Категорія', max_length=50)
    photos = models.JSONField('Фотографії товару', default=list)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Кошик #{self.id} користувача {self.user}"

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} у кількості {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Елемент кошика"
        verbose_name_plural = "Елементи кошика"

class Order(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="ПІБ")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    delivery_method = models.CharField(max_length=50, choices=[
        ('Нова Пошта', 'Нова Пошта'),
        ('Укрпошта', 'Укрпошта'),
        ('Кур’єр', 'Кур’єр'),
    ], verbose_name="Спосіб доставки")
    delivery_address = models.CharField(max_length=255, verbose_name="Адреса доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")
    order_details = models.TextField(verbose_name="Деталі замовлення", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення {self.id} для {self.full_name}"
