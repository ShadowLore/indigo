from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from account.views import AccountView

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),

    path('accounts/', include('account.urls', namespace='account')),
    path('accounts/', AccountView.as_view(), name='accounts'),

    path('checkout/', include('checkout.urls', namespace='checkout')),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
