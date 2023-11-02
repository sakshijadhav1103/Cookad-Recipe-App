from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='Recipes'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('results/', views.results, name='results'),
    path('recipe/<int:recipe_id>/',views.recipe_detail, name='recipe_detail'),
    path('substitutes/', views.substitutes, name='substitutes'),
    path('conversions/', views.conversions, name='conversions'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
