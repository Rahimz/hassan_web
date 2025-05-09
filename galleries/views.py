from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from multimedias.models import Gallery


def GalleriesView(request):
    galleries = Gallery.objects.all()
    context = dict(
        page_title = _("Galleries"),
         navSection='galleries',
         galleries=galleries
    )
    return render(
        request,
        'galleries/galleries.html',
        context
    )


def GalleryDetailsView(request, id):
    gallery = get_object_or_404(Gallery.objects.prefetch_related('images'), id=id)
    context = dict(
        page_title = _("Gallery") + f" | {gallery.name}",
         navSection='galleries',
         gallery=gallery
    )
    return render(
        request,
        'galleries/gallery.html',
        context
    )