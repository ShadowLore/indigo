from django.views.generic import ListView
from mainapp.models import Product
from .models import Order, Cart

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("mainapp:cart-home")
        else:
            order.order_items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("mainapp:cart-home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.order_items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("mainapp:cart-home")


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_items.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.order_items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("mainapp:home")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mainapp:home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:home")


def CartView(request):
    user = request.user

    carts = Cart.objects.filter(user=user)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        order = orders[0]
        return render(request, 'cart/cart.html', {"carts": carts, 'order': order})

    else:
        messages.warning(request, "You do not have an active order")
        return redirect("mainapp:home")


def decreaseCart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_items.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.order_items.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mainapp:cart-home")