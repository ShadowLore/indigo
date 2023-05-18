from django.shortcuts import render
from django.views.generic import ListView
from .models import Customer

from django import views
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


# страница авторизации
class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'account/login.html', context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        context = {
            'form': form
        }
        return render(request, 'account/login.html', context)


# страница регистрации
class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'account/registration.html', context)

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)

        if form.is_valid():

            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()

            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            Customer.objects.create(
                user=new_user,
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'account/registration.html', context)


# страница аккаунта
class AccountView(views.View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer,
        }
        return render(request, 'account/account.html', context)
