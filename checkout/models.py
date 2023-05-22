from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


# типо оплата заказов
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Название')
    address = models.CharField(max_length=180, verbose_name='Город')
    card_num = models.IntegerField(verbose_name='Улица')
    cvv = models.IntegerField(verbose_name='Телефон')

    def __str__(self):
        return f'{self.user.username} Платежный адрес'

    class Meta:
        verbose_name = "Платежный адрес"
        verbose_name_plural = "Платежные адреса"


class BillingForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address', 'card_num', 'cvv']
