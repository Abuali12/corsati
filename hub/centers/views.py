from django.shortcuts import render, redirect
from core.models import Center, State, Subject, Profile
from core.utils import upload_to_supabase
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from core.utils import center_access_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Q
from core.forms import CenterForm
import datetime

# Create your views here.
def centers(request):
    centers= Center.objects.filter(is_verified=True, is_active=True, is_deleted= False)

    q= request.GET.get('q')
    state= request.GET.get('state')
    subject= request.GET.get('subject')

    if q:
        centers= centers.filter(Q(title__icontains=q))

    if state:
        centers= centers.filter(state_id= state)

    if subject:
        centers= centers.filter(subjects__id= subject)

    centers= centers.distinct()
    paged_centers= Paginator(centers, 10)
    page_number= request.GET.get('page')
    page= paged_centers.get_page(page_number)

    context= {
        'centers': centers,
        'paged_centers': page,
        'states': State.objects.all(),
        'subjects': Subject.objects.all(),
        }
    return render(request, 'centers/centers.html', context)

def center(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    center.view_count += 1
    center.save(update_fields=['view_count'])
    courses= center.courses.filter(is_verified=True, is_active=True)
    context= {'center': center, 'courses':courses}
    return render(request, 'centers/center.html', context)

@login_required
@permission_required('core.can_access_dashboard', raise_exception=True)
def centers_dashboard(request):
    owned_centers= Center.objects.filter(owner= request.user)
    staff_centers= request.user.working_centers.all()
    context= {'owned_centers': owned_centers, 'staff_centers': staff_centers}
    return render(request, 'centers/centers_dashboard.html', context)

@login_required

def center_dashboard(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    is_owner= center.owner == request.user
    is_staff= center.staff.filter(id= request.user.id).exists()
    if not (is_owner or is_staff):
        raise PermissionDenied
    else: 
        courses= center.courses.filter(is_deleted=False)
        context={'center':center, 'courses':courses}
        return render(request, 'centers/center_dashboard.html', context)

@login_required
def add_center(request):

    if request.method == 'POST':
        form=CenterForm(request.POST, request.FILES)
        if form.is_valid():
            center=form.save(commit=False)
            center.owner= request.user

            if request.FILES.get('logo'):
                print('uploading...')
                logo_url= upload_to_supabase(
                    request.FILES['logo'],
                    folder= 'centers_logos'
                )
                print(logo_url)
                center.logo_url= logo_url

            center.save()
            form.save_m2m()
            manager_group= Group.objects.get(name='Manager')
            request.user.groups.add(manager_group)
            return redirect('center_dashboard', center.slug)
    else:
            form=CenterForm()
    context={'form':form, 'title': 'إضافة مركز'}
    return render(request, 'centers/add_edit_center.html', context)



@login_required
@center_access_required
@permission_required('core.change_center', raise_exception=True)
def edit_center(request, center_slug):
    center=Center.objects.get(slug=center_slug)

    if center.owner != request.user :
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form=CenterForm(request.POST, request.FILES, instance=center)
        if form.is_valid():
            center=form.save(commit=False)
            center.updated_at= datetime.datetime.now()
            center.save()
            form.save_m2m()
            messages.success(request, "تم تحديث بيانات المركز بنجاح، سيتم مراجعة التغييرات من قبل الإدارة خلال 24 ساعة")
            return redirect('center_dashboard', center_slug)
    else:
        form=CenterForm(instance=center)

    context={'form':form, 'title': 'تعديل المركز'}
    return render(request, 'centers/add_edit_center.html', context)

@login_required
def delete_center(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    center.is_deleted= True
    return redirect('index')

def clear(request):
    return redirect('centers')