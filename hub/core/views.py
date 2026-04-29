from django.shortcuts import render
from .models import TrackingLink
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F

# test push

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def tracked_redirect(request, code):
    link = get_object_or_404(TrackingLink, code=code)

    link.click_count = F('click_count') + 1
    link.save(update_fields=['click_count'])

    return redirect(link.target_url)

