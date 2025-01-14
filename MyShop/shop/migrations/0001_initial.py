# Generated by Django 5.1.4 on 2025-01-06 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='ПІБ')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('delivery_method', models.CharField(choices=[('Нова Пошта', 'Нова Пошта'), ('Укрпошта', 'Укрпошта'), ('Кур’єр', 'Кур’єр')], max_length=50, verbose_name='Спосіб доставки')),
                ('delivery_address', models.CharField(max_length=255, verbose_name='Адреса доставки')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Коментар')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Загальна сума')),
                ('order_details', models.TextField(blank=True, null=True, verbose_name='Деталі замовлення')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва товару')),
                ('desc', models.TextField(verbose_name='Опис товару')),
                ('price', models.FloatField(verbose_name='Ціна товару')),
                ('the_is', models.CharField(max_length=1, verbose_name='Наявність')),
                ('category', models.CharField(max_length=50, verbose_name='Категорія')),
                ('photos', models.JSONField(default=list, verbose_name='Фотографії товару')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Кошик',
                'verbose_name_plural': 'Кошики',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'verbose_name': 'Елемент кошика',
                'verbose_name_plural': 'Елементи кошика',
            },
        ),
    ]
