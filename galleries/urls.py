from django.urls import path
from . import views 

app_name = 'galleries'

urlpatterns = [
    path('<int:id>/', views.GalleryDetailsView, name='gallery_details'),
    path('', views.GalleriesView, name='galleries'),
]
