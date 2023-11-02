from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Recipes.urls')),  # Include your Recipes app URLs
    path('users/', include('users.urls')),  # Include users app URLs
]

if settings.DEBUG: 
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)