from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    is_active = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='Почта')
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, default='default phone')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
