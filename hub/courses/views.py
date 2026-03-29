from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from core.models import Course, Center, Profile, State, Subject
from django.db.models import Q
from django.contrib import messages
from core.forms import CourseForm, LeadForm
from core.utils import center_access_required
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

def course(request, course_slug):

    course= Course.objects.get(slug= course_slug)
    course.view_count += 1
    course.save(update_fields=['view_count'])

    form= LeadForm()
    context= {'course': course, 'form': form}
    return render(request, 'courses/course.html', context)

# ============= course lead view ============

def course_lead(request, course_slug):
    course= Course.objects.get(slug= course_slug)
    if request.method == 'POST':
        form= LeadForm(request.POST)
        if form.is_valid():
            lead= form.save(commit=False)
            lead.course= course
            lead.lead_type= 'course'
            lead.save()
            messages.success(request, "تم إرسال طلبك بنجاح")
            
    
    return redirect('course', course_slug)

# ============= CRUD views ==================

@login_required
@permission_required('core.add_course', raise_exception=True)
def add_course(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    if request.method == 'POST':
        form=CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.center= center
            course.created_by= request.user
            course.save()
            form.save_m2m()
            return redirect('center_dashboard', center.slug)
    else:
        form= CourseForm()
    context= {'form':form, 'title':'إضافة دورة'}
    return render(request, 'courses/add_edit_course.html' , context)

@login_required
@permission_required('core.change_course', raise_exception=True)
def edit_course(request, course_slug):
    course=Course.objects.get(slug=course_slug)
 
    if request.method == 'POST':
        form=CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.approved=False
            course.save()
            form.save_m2m()
            return redirect('center_dashboard', course.center.slug)
    else:
        form=CourseForm(instance=course)

    context= {'form': form, 'title': 'تعديل الدورة'}
    return render(request, 'courses/add_edit_course.html', context)

@login_required
@center_access_required
def delete_course(request, course_slug):

    course= Course.objects.get(slug= course_slug)
    course.delete()
    messages.success(request, "تم حذف الدورة بنجاح")
    return redirect('center_dashboard', course.center.slug)

@login_required
@center_access_required
def deactivate(request, course_slug):

    course= Course.objects.get(slug= course_slug)
    course.is_active= False
    course.save()
    return redirect('center_dashboard', course.center.slug)

def clear(request):
    return redirect('courses')
