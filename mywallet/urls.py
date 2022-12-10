from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('ativos/', include('ativos.urls')),
    path('admin/', admin.site.urls),
]