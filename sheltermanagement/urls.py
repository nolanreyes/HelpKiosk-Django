from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='shelter_base'),
    path('dashboard/', views.dashboard, name='shelter_dashboard'),
    path('rooms/', views.rooms_display, name='shelter_rooms'),
    path('guests/', views.guests, name='shelter_guests'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('remove_guest/<str:wallet_address>/', views.remove_guest, name='remove_guest'),
    path('management/', views.management, name='shelter_management'),
    path('rooms/<uuid:id>/', views.room_details, name='shelter_room_details'),
    path('rooms/<uuid:room_id>/add_bed/', views.add_bed, name='shelter_add_bed'),
    path('rooms/<uuid:room_id>/beds/<uuid:bed_id>/edit/', views.edit_bed, name='shelter_edit_bed'),
    path('rooms/<uuid:room_id>/beds/<uuid:bed_id>/delete/', views.edit_bed, name='shelter_delete_bed'),
    path('allocate-bed/<str:wallet_address>/', views.allocate_bed_to_guest, name='shelter_allocate_bed_to_guest'),
    path('allocate-bed-flutter/', views.allocate_bed_to_guest_flutter, name='shelter_allocate_bed_to_guest_flutter'),
    path('beds/<uuid:bed_id>/free-up/', views.free_up_bed, name='shelter_free_up_bed'),
    path('authenticate_guest/', views.authenticate_guest, name='authenticate_guest'),
]
