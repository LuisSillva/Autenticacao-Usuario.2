from django.urls import path
from autenticacao_app import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('cadastro/', views.user_cadastro, name='cadastro'),
    path('home', views.home, name='home'),
    path('signout', views.user_signout, name='signout')
]
