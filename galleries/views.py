from django.shortcuts import render
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
