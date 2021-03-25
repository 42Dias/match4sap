from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('abcdefghijklrmnopqrs1234567/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Local Apps
    path('', include('pages.urls')),
    path('headhunters/', include('headhunters.urls')),
    path('users/', include('users.urls')),
    path('professionals/', include('professionals.urls')),
    path('orders', include('orders.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
