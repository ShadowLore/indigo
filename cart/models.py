from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model
from mainapp.models import Product


User = get_user_model()


# МОДЕЛЬ корзины
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} {self.item.name}'

    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


# МОДЕЛЬ заказа
class Order(models.Model):
    order_items = models.ManyToManyField(Cart, verbose_name='Товары в заказе')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    ordered = models.BooleanField(default=False, verbose_name='Заказной')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    paymentId = models.CharField(max_length=200, blank=True, null=True, verbose_name='ID оплаты')
    orderId = models.CharField(max_length=200, blank=True, null=True, verbose_name='ID заказа')

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total()

        return total

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
