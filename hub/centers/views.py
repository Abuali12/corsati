from django.shortcuts import render
from core.models import Center, Course

# Create your views here.
def centers(request):
    centers= Center.objects.all()
    context= {'centers': centers}
    return render(request, 'centers/centers.html', context)

def center(request, center_id):
    center= Center.objects.get(id= center_id)
    courses= Course.objects.filter(center= center)
    context= {'center': center, 'courses':courses}
    return render(request, 'centers/center.html', context)