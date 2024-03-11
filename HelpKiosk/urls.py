from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assistanceapp/', include('assistanceapp.urls')),
    path('sheltermanagement/', include('sheltermanagement.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
