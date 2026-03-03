from django.shortcuts import render, redirect
from core.models import Course, Center, Profile, State, Subject
from django.db.models import Q
from core.forms import CourseForm
import datetime

# Create your views here.
def courses(request):
    courses= Course.objects.filter(is_verified= True, is_active= True).select_related('center').prefetch_related('subjects')

    q= request.GET.get('q')
    subject= request.GET.get('subject')
    type= request.GET.get('type')
    price= request.GET.get('price')

    if q:
        courses= courses.filter(Q(title__icontains= q))

    if subject: 
        courses= courses.filter(subjects__id= subject)
    
    if type:
        courses= courses.filter(course_type= type)

    if price:

        try:
            price= float(price)
            courses= courses.filter(price__lte= price)

        except ValueError:
            pass

    courses= courses.distinct()

    context={
        'courses': courses,
        'subjects': Subject.objects.all(),
        'states': State.objects.all(),
        'type': Course.TYPE}
    
    return render(request, 'courses/courses.html',context)

def course(request, course_id):
    course= Course.objects.get(id= course_id)
    course.view_count += 1
    course.save(update_fields=['view_count'])
    context= {'course': course}
    return render(request, 'courses/course.html', context)

def add_course(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    if request.user.profile.center == center:
        if request.method == 'POST':
            form=CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course=form.save(commit=False)
                course.center= center
                course.created_by= request.user.profile
                course.save()
                form.save_m2m()
        else:
            form= CourseForm()
        context= {'form':form}
    return render(request, 'courses/add_edit_course.html' , context)

def edit_course(request, course_id):
    course=Course.objects.get(id=course_id)
    profile= Profile.objects.get(user= request.user)
    if profile.center == course.center:  #change to check if user in center.staff
        if request.method == 'POST':
            form=CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course=form.save(commit=False)
                course.approved=False
                course.updated_at= datetime.datetime.now
                course.save()
                form.save_m2m()
        else:
            form=CourseForm(instance=course)

    return render(request, 'courses/add_edit_course.html')

def delete_course(request, course_id):
    return render(request, 'courses/delete_course.html')

def clear(request):
    return redirect('courses')
