from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from timeline.models import Entry
from multimedias.models import Image


def TimeLineView(request, filter='main'):
    entries = Entry.actives.all()
    images = []
    if filter == 'all':
        images = Image.objects.filter(date__isnull=False).order_by('date')
        
    
    results = [x for x in entries] + [y for y in images]
    sorted_timeline = sorted(results, key=lambda x: x.date)
    
    context = dict(
        page_title = _("Timeline"),
        navSection='timeline',
        entries=entries,
        sorted_timeline=sorted_timeline,
        filter=filter
         
    )
    return render(
        request,
        'timeline/timeline.html',
        context
    )