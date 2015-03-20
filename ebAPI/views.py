from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.cache import cache
import urllib2
"""
ujson is a quicker parser than json
"""
import ujson
# Create your views here.

INDEX_URL = "https://www.eventbriteapi.com/v3/categories/?token=BKKRDKVUVRC5WG4HAVLT"
RESULT_URL = "https://www.eventbriteapi.com/v3/events/search/?categories="


def index(request):
    jsonCategories = urllib2.urlopen(INDEX_URL).read()
    categories = ujson.loads(jsonCategories)["categories"]
    context = {
        "categories":categories,
        }
    return render(request,"index.html",context)

def result(request):
    preference = request.GET.getlist("prefer")
    try: page = request.GET["page"]
    except: page = "1"
    categories = ",".join(preference)
    key = categories+page
    """
    using cached page if applicable
    """
    cached_result = cache.get(key)
    if cached_result != None:
        return cached_result
    context = ujson.loads(
        urllib2.urlopen(
            RESULT_URL+categories+"&page="+page+"&token=BKKRDKVUVRC5WG4HAVLT#"
        ).read()
    )
    base_url = "?"+"prefer="+preference[0]+"&prefer="+preference[1]+"&prefer="+preference[2]+"&page="
    context["previous_url"] = base_url+str(int(page)-1)
    context["next_url"] = base_url+str(int(page)+1)
    cached_result = render(request,"result.html",context)
    cache.set(key,cached_result)
    return cached_result