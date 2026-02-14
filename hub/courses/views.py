from django.shortcuts import render, redirect
from core.models import Course, Center, Profile
from core.forms import CourseForm
import datetime

# Create your views here.
def courses(request):
    courses= Course.objects.filter(is_verified= True, is_active= True)
    context={'courses': courses}
    return render(request, 'courses/courses.html',context)

def course(request, course_slug):
    course= Course.objects.get(slug= course_slug)
    course.view_count += 1
    course.save(update_fields=['view_count'])
    context= {'course': course}
    return render(request, 'courses/course.html', context)

def add_course(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    if request.user.profile.center == center:
        if request.method == 'POST':
            form=CourseForm(request)
            if form.is_valid():
                course=form.save(commit=False)
                course.center= center
                course.created_by= request.user.profile
                course.save()
        else:
            form= CourseForm()
        context= {'form':form}
    else:
        return redirect('index') # add permisson denied here
    return render(request, 'courses/add_edit_course.html' , context)

def edit_course(request, course_id):
    course=Course.objects.get(id=course_id)
    profile= Profile.objects.get(user= request.user)
    if profile.center == course.center:
        if request.method == 'POST':
            form=CourseForm(request)
            if form.is_valid():
                course=form.save(commit=False)
                course.approved=False
                course.updated_at= datetime.datetime.now
                course.save()
        else:
            form=CourseForm(instance=course)
    else:
        return redirect('index') # add permisson denied here

    return render(request, 'courses/add_edit_course.html')

def delete_course(request, course_id):
    return render(request, 'courses/delete_course.html')

def clear(request):
    return redirect('courses')
