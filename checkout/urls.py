from django.urls import path
from .views import checkout, orderView

app_name = "checkout"

urlpatterns = [
    path('checkout/', checkout, name="index"),
    path('my-orders/', orderView, name="order")
]
