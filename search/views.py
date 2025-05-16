from django.shortcuts import render
# from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from multimedias.models import Image, Gallery
from timeline.models import Entry


def normalize_numerals(text):
    # Mapping of Persian numerals to English
    persian_to_english = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    for persian, english in persian_to_english.items():
        text = text.replace(persian, english)
    return text


def SearchView(request):
    query = request.GET.get('query')
    results = dict(
        images=None,
        entries=None
    )
    
    if query:
        
        query = query.replace('/', ' ')
        query = ''.join(c for c in query if c.isalnum() or c.isspace())
        query = query.strip()
        
        normalized_query = normalize_numerals(query)
        
        # images = Image.actives.annotate(
        #     search=SearchVector('title', 'description')
        # ).filter(search=query)
        # entries = Entry.objects.annotate(
        #     search=SearchVector('title', 'description')        
        # ).filter(search=query)
        
        images = Image.actives.filter(
             Q(title__icontains=query) | 
            Q(title__icontains=normalized_query) |
            Q(description__icontains=query) |
            Q(description__icontains=normalized_query) |
            Q(h_year__icontains=query) |
            Q(h_year__icontains=normalized_query)
        )
        entries = Entry.actives.filter(
            Q(title__icontains=query) | 
            Q(title__icontains=normalized_query) |
            Q(description__icontains=query) |
            Q(description__icontains=normalized_query) |
            Q(h_year__icontains=query) |
            Q(h_year__icontains=normalized_query)
        )
        galleries = Gallery.objects.filter(
            Q(name__icontains=query) | 
            Q(name__icontains=normalized_query) |
            Q(description__icontains=query) |
            Q(description__icontains=normalized_query)
        )
        if images:
            results['images'] = images
        
        if entries:
            results['entries'] = entries
        
        if galleries:
            results['galleries'] = galleries
    
    context = dict(
        page_title = 'نتایج جستجو',
        navSection='search',
        results = results,
        query=query
    )
    
    return render(
        request, 
        'search/search.html',
        context
    )
