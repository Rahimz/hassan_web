from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from multimedias.models import Gallery, Image


def HomeView(request):
    images = Image.objects.filter(gallery__zone='gallery').order_by('?')[:4]
    certs = Image.objects.filter(gallery__zone='cert').order_by('?')[:4]
    context = dict(
        page_title = _("Home"),
        navSection='home', 
        images=images,
        certs=certs
    )
    return render(
        request,
        'generals/home.html',
        context
    )


def CertificatesView(request):    
    gallery = Gallery.objects.filter(zone=Gallery.ZoneChoices.CERT).prefetch_related('images').last()
    context = dict(
        page_title = _("Gallery") + f" | {gallery}",
         navSection='certificates',
         gallery=gallery
    )
    return render(
        request,
        'galleries/gallery.html',
        context
    )