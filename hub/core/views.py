from django.shortcuts import render
from .models import Course, Center

# Create your views here.
def index(request):
    return render(request, 'core/index.html')



