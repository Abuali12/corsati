from django.shortcuts import render
from core.models import Course

# Create your views here.
def courses(request):
    courses= Course.objects.all()
    context={'courses', courses}
    return render(request, 'courses/courses.html',context)

def course(request, course_id):
    course= Course.objects.get(id= course_id)
    context= {'course': course}
    return render(request, 'courses/course.html', context)
