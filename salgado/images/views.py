from django.shortcuts import render
from django.http import JsonResponse

from django.db.models.functions import Now

from images.models import Image
# Create your views here.

def v1_get_image(request):
    try:
        image = Image.objects.filter(viewable=True).order_by("last_shown")[0]
    except IndexError:
        return JsonResponse({ "status": "error", "refresh_interval": 3600})
    
    image.last_shown = Now()
    image.save()
    return JsonResponse({ "status": "ok", "image": image.converted_image.url, "refresh_interval": 84600 })