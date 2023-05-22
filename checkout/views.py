from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from django.utils.crypto import get_random_string

from .models import BillingForm, BillingAddress
from django.contrib import messages

import stripe
from django.conf import settings

stripe.api_key = "sk_test_51N8dHoDktWkjNp7TYMfQC816pslV5vD0f5viwkRLBAk34VrndsilmT5CvywcK8fYq8cCuhcXhicMMCCNeADTSRct007cP28Ow7"

stripe.PaymentIntent.create(
  amount=500,
  currency="gbp",
  payment_method="pm_card_visa",
)


# страница формы добавления адреса
def checkout(request):
    form = BillingForm

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    context = {"form": form, "order_items": order_items, "order_total": order_total}

    saved_address = BillingAddress.objects.filter(user=request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
    if request.method == "POST":
        saved_address = BillingAddress.objects.filter(user=request.user)
        if saved_address.exists():

            savedAddress = saved_address.first()
            form = BillingForm(request.POST, instance=savedAddress)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
        else:
            form = BillingForm(request.POST)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()

    return render(request, 'checkout/index.html', context)

# страница оплаты
def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_total = order_qs[0].get_totals()
    totalCents = float(order_total * 100);
    total = round(totalCents, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
                                      currency='rub',
                                      description=order_qs,
                                      source=request.POST['stripeToken'])
        print(charge)

    return render(request, 'checkout/payment.html', {"key": key, "total": total})


# оплата через систему платежей strip
def charge(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order_total = order.get_totals()
    totalCents = int(float(order_total * 100));
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=totalCents,
                                      currency='rub',
                                      description=order,
                                      source=request.POST['stripeToken'])
        if charge.status == "succeeded":
            orderId = get_random_string(length=16,
                                        allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            print(charge.id)
            order.ordered = True
            order.paymentId = charge.id
            order.orderId = f'#{request.user}{orderId}'
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
                item.purchased = True
                item.save()
        return render(request, 'checkout/charge.html')


# страница заказов
def orderView(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            "orders": orders
        }
    except:
        messages.warning(request, "You do not have an active order")
        return redirect('/')
    return render(request, 'checkout/order.html', context)
