from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required, permission_required
from core.models import Course, Center, Profile, State, Subject
from core.utils import upload_to_supabase
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.forms import CourseForm, LeadForm
from core.utils import center_access_required
import datetime

# Create your views here.
def courses(request):
    courses= Course.objects.filter(is_verified= True, is_active= True, is_deleted=False).select_related('center').prefetch_related('subjects')


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
    p= Paginator(courses, 20)
    page_number= request.GET.get("page")
    page= p.get_page(page_number)

    context={
        'courses': page,
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
            messages.success(request, "تم إرسال طلبك بنجاح، سيتواصل معك المركز قريبا!")

            # center email
            if course.center.contact_email:
                subject = 'منصة كورساتي: طلب تسجيل لدورة'

                html_content = render_to_string(
                    'emails/center_alert.html',{
                        'student_name': lead.student_name,
                        'student_email': lead.student_email,
                        'student_phone': lead.student_phone,
                        'note': lead.note,
                        'course_title': course.title,

                    }
                )
                text_content = strip_tags(html_content)

                center_email= course.center.contact_email
                
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'hassan.mohemmad777@gmail.com',
                    [center_email]
                )

                email.attach_alternative(html_content, "text/html")
                email.send()

                #user email
            if lead.student_email: 
                subject= 'تم قبول طلبك'
                html_content= render_to_string(
                    'emails/application_accepted.html',{
                        'student_name':lead.student_name,
                        'course_name': course.title,
                        'center_name': course.center.title,
                        'center_phone': course.center.contact_phone,
                    }
                )
                text_content= strip_tags(html_content)

                email= EmailMultiAlternatives(
                    subject,
                    text_content,
                    'hassan.mohemmad777@gmail.com',
                    [lead.student_email]
                )

                email.attach_alternative(html_content, 'text/html')
                email.send(fail_silently=True)

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

            if request.FILES.get('image'):
                print('uploading...')
                image_url= upload_to_supabase(
                    request.FILES['image'],
                    folder='courses',
                )
                print(image_url)
                course.image_url=image_url


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
        form=CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course=form.save(commit=False)
            course.save()
            form.save_m2m()
            return redirect('center_dashboard', course.center.slug)
    else:
        form=CourseForm(instance=course)

    context= {'form': form, 'title': 'تعديل الدورة'}
    return render(request, 'courses/add_edit_course.html', context)

@login_required
@permission_required('core.delete_course', raise_exception=True)
def delete_course(request, course_slug):

    course= Course.objects.get(slug= course_slug)
    course.is_deleted= True
    course.save(update_fields=['is_deleted'])
    messages.success(request, "تم حذف الدورة بنجاح")
    return redirect('center_dashboard', course.center.slug)

@login_required
@permission_required('core.delete_course', raise_exception=True)
def toggle_activity(request, course_slug):

    course= Course.objects.get(slug= course_slug)
    course.is_active= not course.is_active
    course.save()
    return redirect('center_dashboard', course.center.slug)

def clear(request):
    return redirect('courses')
