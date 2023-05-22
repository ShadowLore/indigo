from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# модель категории
class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    primaryCategory = models.BooleanField(default=False)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("mainapp:category-detail", kwargs={'pk': self.pk})

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# модель продукта
class Product(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mainapp:product-detail", kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
