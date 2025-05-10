from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from timeline.models import Entry


def TimeLineView(request):
    entries = Entry.actives.all()
    context = dict(
        page_title = _("Timeline"),
        navSection='timeline',
        entries=entries,
         
    )
    return render(
        request,
        'timeline/timeline.html',
        context
    )