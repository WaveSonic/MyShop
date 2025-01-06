import json
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart, CartItem
from .forms import OrderForm

def home_page(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    products_list = Product.objects.all()

    # Отримуємо параметри сортування і кількості товарів
    sort_by = request.GET.get('sort_by', '')
    per_page = request.GET.get('per_page', 12)

    # Застосовуємо сортування на основі параметра
    if sort_by == 'availability':
        products_list = products_list.order_by('-the_is')
    elif sort_by == 'name_asc':
        products_list = products_list.order_by('name')
    elif sort_by == 'name_desc':
        products_list = products_list.order_by('-name')
    elif sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')

    # Пагінація
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 12  # Якщо значення не є числом, встановлюємо 12
    paginator = Paginator(products_list, per_page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    data = {
        'categories': [{'name': x, 'url': x} for x in categories],
        'products': products,
        'sort_by': sort_by,  # Додаємо значення сортування в контекст
        'per_page': per_page  # Додаємо кількість товарів в контекст
    }
    return render(request, 'shop/index.html', data)


def category_list(request, category):
    categories = Product.objects.values_list('category', flat=True).distinct()
    products_list = Product.objects.filter(category=category)

    sort_by = request.GET.get('sort_by', '')
    per_page = request.GET.get('per_page', 12)

    if sort_by == 'availability':
        products_list = products_list.order_by('-the_is')
    elif sort_by == 'name_asc':
        products_list = products_list.order_by('name')
    elif sort_by == 'name_desc':
        products_list = products_list.order_by('-name')
    elif sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')


    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 12  # Якщо значення не є числом, встановлюємо 12

    # Пагінація
    paginator = Paginator(products_list, per_page)  # Розбиваємо на сторінки по обраній кількості товарів
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)  # Отримати товари для поточної сторінки
    data = {
        'categories': [{'name': x, 'url': x} for x in categories],
        'products': products,
        'per_page': per_page,
        'sort_by': sort_by
    }
    return render(request, 'shop/index.html', data)


def product(request, product_id):
    categories = Product.objects.values_list('category', flat=True).distinct()
    product_ = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category=product_.category).exclude(id=product_.id).order_by('?')[:2]
    data = {
        'categories': [{'name': x, 'url': x} for x in categories],
        'product': product_,
        'related_products': related_products
    }
    return render(request, 'shop/product.html', data)


def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))[:10]
        results = [{'id': product.id, 'name': product.name, 'price': product.price, 'desc': product.desc} for product in products]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Отримуємо кількість з форми

    if request.user.is_authenticated:
        # Отримуємо або створюємо кошик для авторизованого користувача
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Додаємо товар до кошика або оновлюємо кількість
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity  # Якщо товар вже є, збільшуємо кількість
        else:
            cart_item.quantity = quantity
        cart_item.save()
    else:
        # Якщо користувач не авторизований, використовуємо сесію
        cart = request.session.get('cart', {})

        # Якщо товар вже є в кошику, збільшуємо кількість
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {'quantity': quantity, 'price': str(product.price)}

        # Оновлюємо сесію
        request.session['cart'] = cart

    return redirect('cart')


def cart_view(request):
    categories = Product.objects.values_list('category', flat=True).distinct()

    cart_items_with_total = []
    total_price = 0

    if request.user.is_authenticated:
        # Витягуємо кошик авторизованого користувача
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        for item in cart_items:
            item_total_price = item.product.price * item.quantity
            total_price += item_total_price
            cart_items_with_total.append({
                'product': item.product,
                'quantity': item.quantity,
                'total_price': item_total_price,
                'id': item.id  # для оновлення/видалення товару
            })
    else:
        # Витягуємо кошик з сесії для анонімного користувача
        cart = request.session.get('cart', {})

        for product_id, details in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total_price = float(details['quantity']) * float(details['price'])
            total_price += item_total_price
            cart_items_with_total.append({
                'product': product,
                'quantity': details['quantity'],
                'total_price': item_total_price,
                'id': product_id
            })

    data = {
        'categories': [{'name': x, 'url': x} for x in categories],
        'cart_items': cart_items_with_total,
        'total_price': total_price,
    }
    return render(request, 'shop/cart.html', data)


def update_cart_item(request, item_id):
    if request.user.is_authenticated:
        # Якщо користувач автентифікований, працюємо з кошиком, прив'язаним до користувача
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                item.quantity = quantity
                item.save()

    else:
        # Для анонімних користувачів працюємо з сесією
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            # Оновлюємо кількість товару у сесійному кошику
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[str(item_id)]['quantity'] = quantity
                request.session['cart'] = cart

    return redirect('cart')


def delete_cart_item(request, item_id):
    if request.user.is_authenticated:
        # Якщо користувач автентифікований, працюємо з кошиком, прив'язаним до користувача
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if request.method == 'POST':
            item.delete()

    else:
        # Для анонімного користувача працюємо з сесією
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            # Видаляємо товар із сесійного кошика
            del cart[str(item_id)]
            request.session['cart'] = cart

    return redirect('cart')



def checkout_view(request):
    categories = Product.objects.values_list('category', flat=True).distinct()

    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        # Для авторизованого користувача
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            for item in cart.items.all():
                total_item_price = item.product.price * item.quantity
                total_price += total_item_price
                cart_items.append({
                    'product': item.product,
                    'quantity': item.quantity,
                    'total_price': total_item_price
                })
    else:
        # Для анонімного користувача використовуємо сесію для зберігання кошика
        session_cart = request.session.get('cart', {})
        for product_id, item in session_cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item['quantity']
            total_item_price = product.price * quantity
            total_price += total_item_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_item_price
            })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Створюємо замовлення
            order = form.save(commit=False)
            order.total_price = total_price

            # Формуємо деталі замовлення у вигляді тексту
            order_details = []
            for item in cart_items:
                details = f"{item['product'].name} - {item['quantity']} шт. - {item['product'].price} грн"
                order_details.append(details)

            # Зберігаємо деталі у вигляді текстового рядка
            order.order_details = "\n".join(order_details)
            order.save()

            if request.user.is_authenticated:
                # Очищуємо кошик для авторизованого користувача
                cart.items.all().delete()
            else:
                # Очищуємо сесію для анонімного користувача
                request.session['cart'] = {}
                request.session.modified = True

            # Перенаправляємо на сторінку успіху замовлення
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'total_price': total_price,
        'cart_items': cart_items,
        'categories': [{'name': x, 'url': x} for x in categories]
    })



def order_success(request, order_id):
    categories = Product.objects.values_list('category', flat=True).distinct()
    data = {
        'categories': [{'name': x, 'url': x} for x in categories],
        'order_id': order_id
    }
    return render(request, 'shop/order_success.html', data)