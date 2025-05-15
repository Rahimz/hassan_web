from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from multimedias.models import Gallery, Image


def GalleriesView(request):
    galleries = Gallery.objects.filter(zone=Gallery.ZoneChoices.GALLERY)
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
    
def ImageDetailsView(request, short_uuid):
    image = get_object_or_404(Image, short_uuid=short_uuid)
    context = dict(
        page_title = f"تصویر | {image.title}",
        navSection='galleries',
        image=image
    )
    return render(
        request,
        'galleries/image_details.html',
        context
    )