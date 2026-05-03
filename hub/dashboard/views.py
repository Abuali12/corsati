from django.shortcuts import render, redirect, get_object_or_404
from core.models import Center, Lead
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count
from django.core.paginator import Paginator


# Create your views here.

@login_required
@permission_required('core.can_access_dashboard', raise_exception=True)
def centers_dashboard(request):

    owned_centers= Center.objects.filter(owner= request.user)

    staff_centers= request.user.working_centers.all()

    context= {'owned_centers': owned_centers, 'staff_centers': staff_centers}

    return render(request, 'dashboard/centers_dashboard.html', context)


@login_required
@permission_required('core.can_access_dashboard', raise_exception=True)
def center_dashboard(request, center_slug):

    center= get_object_or_404(Center, slug= center_slug)

    is_owner= center.owner == request.user

    is_staff= center.staff.filter(id= request.user.id).exists()

    if not (is_owner or is_staff):
        raise PermissionDenied
    
    else: 

        courses= center.courses.filter(is_deleted=False).annotate(lead_count= Count('leads'))
        
        leads_summery= Lead.objects.filter(center=center, course__is_deleted= False).aggregate(
            total= Count('id'),
            new= Count('id', filter=Q(status= 'new')),
            contacted= Count('id', filter=Q(status= 'contacted'))
        )

        context={
            'center':center,
            'courses':courses.order_by('-lead_count'),
            'leads_summery':leads_summery,
        }

        return render(request, 'dashboard/center_dashboard.html', context)


@login_required
@permission_required('core.can_access_dashboard', raise_exception=True)
def leads(request, center_slug):

    center= get_object_or_404(Center, slug=center_slug)

    leads= Lead.objects.filter(center= center).select_related('course')

    paginator= Paginator(leads, 20)
    page= request.GET.get('page')
    leads_page= paginator.get_page(page)

    context={
        'center': center,
        'leads': leads_page,
    }
    return render(request, 'dashboard/leads.html', context)