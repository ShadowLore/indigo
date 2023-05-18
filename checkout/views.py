from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from .models import BillingForm, BillingAddress
from django.contrib import messages


# страница типо оплаты
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
