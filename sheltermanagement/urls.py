from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.rooms_display, name='rooms'),
    path('guests/', views.guests, name='guests'),
    path('management/', views.management, name='management'),
    path('rooms/<uuid:id>/', views.room_details, name='room_details'),
    path('rooms/<uuid:room_id>/add_bed/', views.add_bed, name='add_bed'),
    path('rooms/<uuid:room_id>/beds/<uuid:bed_id>/edit/', views.edit_bed, name='edit_bed'),
    path('rooms/<uuid:room_id>/beds/<uuid:bed_id>/delete/', views.edit_bed, name='delete_bed'),
    path('allocate-bed/<str:wallet_address>/', views.allocate_bed_to_guest, name='allocate_bed_to_guest'),
    path('beds/<uuid:bed_id>/free-up/', views.free_up_bed, name='free_up_bed'),
]
