from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
