from django.urls import path
from . import views 

app_name = 'galleries'

urlpatterns = [
    path('image/<str:short_uuid>/', views.ImageDetailsView, name='image_details'),
    path('<int:id>/', views.GalleryDetailsView, name='gallery_details'),
    path('', views.GalleriesView, name='galleries'),
]
