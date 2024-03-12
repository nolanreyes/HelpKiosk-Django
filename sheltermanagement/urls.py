from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.rooms_display, name='rooms'),
    path('beds/', views.beds, name='beds'),
    path('guests/', views.guests, name='guests'),
    path('management/', views.management, name='management'),
    path('rooms/<uuid:id>/', views.room_details, name='room_details'),
]
