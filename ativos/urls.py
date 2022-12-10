from django.urls import path
from . import views

urlpatterns = [
    path('ações', views.GetPostAtivosBRL.as_view(), name='Lista-de-Ativos'),
    #path('fiis', views.ListarAtivos, name='index'),
    #path('criptos', views.ListarAtivos, name='index'),
    #path('stocks', views.ListarAtivos, name='index'),
    #path('reits', views.ListarAtivos, name='index'),
    #path('etfs', views.ListarAtivos, name='index'),
]