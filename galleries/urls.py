from django.urls import path
from . import views 

app_name = 'galleries'

urlpatterns = [
    path('', views.GalleriesView, name='galleries'),
]
