from django.urls import path
from .views import checkout, orderView, payment, charge

app_name = "checkout"

urlpatterns = [
    path('checkout/', checkout, name="index"),
    path('payment/', payment, name="payment"),
    path('charge/', charge, name="charge"),
    path('my-orders/', orderView, name="order"),
]
