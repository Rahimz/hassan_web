from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
    path('filter/<str:filter>/', views.TimeLineView, name='timeline_filter'),
    path('', views.TimeLineView, name='timeline'),
]
