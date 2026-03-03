from django.shortcuts import render, redirect
from core.models import Center, State, Subject, Profile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from core.utils import center_access_required
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

    context= {
        'centers': centers,
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
@center_access_required
def center_dashboard(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    courses= center.courses.all()
    context={'center':center, 'courses':courses}
    return render(request, 'centers/center_dashboard.html', context)

@login_required
def add_center(request):

    if request.method == 'POST':
        form=CenterForm(request.POST, request.FILES)
        if form.is_valid():
            center=form.save(commit=False)
            center.owner= request.user
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
            center.is_verified=False
            center.updated_at= datetime.datetime.now()
            center.save()
            form.save_m2m()
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