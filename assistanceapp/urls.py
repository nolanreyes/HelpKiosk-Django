from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet
from .views import GetWeatherData

router = DefaultRouter()
router.register(r'locations', LocationViewSet)

urlpatterns = [
    # Login logout urls
    # path('register/', views.login_page, name='register'),
    path('login/', views.login_page, name='assistance_login'),
    path('logout/', views.logout_user, name='assistance_logout'),
    # app paths
    path('', views.base, name='assistance_base'),
    path('map/', views.map_view, name='assistance_map'),
    path('manageLocations/', views.manage_locations, name='manageLocations'),
    path('editLocation/<str:resource_name>/', views.edit_location, name='editLocation'),
    path('deleteLocation/<str:resource_name>/', views.delete_location, name='deleteLocation'),
    # RESTFUL
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/weather/', GetWeatherData.as_view(), name='get_weather'),
]
