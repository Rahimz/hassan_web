from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def TimeLineView(request):
    context = dict(
        page_title = _("Timeline"),
         navSection='timeline',
         
    )
    return render(
        request,
        'timeline/timeline.html',
        context
    )