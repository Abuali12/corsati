from django.shortcuts import render, redirect
from core.models import Center, Course, Profile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from core.forms import CenterForm
import datetime

# Create your views here.
def centers(request):
    centers= Center.objects.filter(is_verified=True, is_active=True)
    context= {'centers': centers}
    return render(request, 'centers/centers.html', context)

def center(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    courses= center.courses.filter(is_verified=True, is_active=True)
    context= {'center': center, 'courses':courses}
    return render(request, 'centers/center.html', context)

@login_required
def center_dashboard(request, center_slug):
    center= Center.objects.get(slug= center_slug)
    courses= center.courses.all()
    context={'center':center, 'courses':courses}
    return redirect(request, 'centers/center_dashboard.html', context)

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
            return redirect('index')
    else:
            form=CenterForm()
    context={'form':form}
    return render(request, 'centers/add_edit_center.html', context)

@login_required
def edit_center(request, center_slug):
    profile=Profile.objects.get(user=request.user)
    center=Center.objects.get(slug=center_slug)

    if profile.center == center and profile.job_title == 'manager':
        if request.method == 'POST':
            form=CenterForm(request.POST, request.FILES)
            if form.is_valid():
                center=form.save(commit=False)
                center.is_verified=False
                center.updated_at= datetime.datetime.now()
                center.save()
                return redirect('center', center_slug)
        else:
            form=CenterForm(instance=center)
        context={'form':form}
    else:
        return redirect('index') #add permisson

    return render(request, 'centers/add_edit_center.html', context)

@login_required
def delete_center(request, center_slug):
    return render(request, 'centers/delete_center.html')

def clear(request):
    return redirect('centers')