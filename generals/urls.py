from django.urls import path
from . import views

app_name = 'generals'


urlpatterns = [
    path('certificates/', views.CertificatesView, name='certificates'),
    path('', views.HomeView, name='home'),
]
