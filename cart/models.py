from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model
from mainapp.models import Product

# Get the user model
User = get_user_model()


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total()

        return total

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
