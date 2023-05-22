from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import ProductFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views import View

from django.db.models import Q

# главная страница


def home(request):
    products = Product.objects.all().order_by('-id')[:6]
    context = {
        'products': products,
    }
    return render(request, 'mainapp/home.html', context)


# страница с категориями

def category(request, *args, **kwargs):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
    }
    return render(request, 'mainapp/catalog.html', context, *args, **kwargs)


# поиск продукции

def search(request):
    queryset = Product.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'mainapp/search_bar.html', context)

# пагинатор, пока никуда не вошел, в планах он пойдет на страницу с продуктавми

# def home(request):
#   products = Product.objects.all().order_by('-id')[:5]
#  paginator = Paginator(products, 6)
# page = request.GET.get('page')
# try:
#   products = paginator.page(page)
# except PageNotAnInteger:
#     products = paginator.page(1)
# except EmptyPage:
#    products = paginator.page(paginator.num_pages)
# vars = dict(
#     products=products,
# )
# return render(request, 'mainapp/home.html', vars)


# страница о нас


def about(request):
    return render(request, 'mainapp/about.html')


# страница о доставке

def about_delivery(request):
    return render(request, 'mainapp/about_delivery.html')


# страница с контактами

def contacts(request):
    return render(request, 'mainapp/contacts.html')


# страница просмотра продукта

class ProductDetailView(DetailView):
    model = Product


# страница просомтра категории
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'mainapp/catalog/category.html'
    context_object_name = 'category'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        queryset = Product.objects.all().filter(category_id=self.category.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Продукты из категории: {self.category.title}'
        return context


# страница создания нового продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'price', 'category', 'slug']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# страница обновки продукта
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'price', 'category', 'slug']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


# страница удаления продукции
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


# страница создания новой категории
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title', 'image', 'author']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# страница обновки категории
class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    slug_field = 'id'
    fields = ['title', 'image', 'author']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False


# страница удаления категории
class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    slug_field = 'id'
    success_url = '/'

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False


# страница редактирования категории и продукта
class Redac(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/redac.html')


# попытка фильтровать продукты по категориям
class List_product(ListView):
    model = Product
    template_name = 'mainapp/list_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context