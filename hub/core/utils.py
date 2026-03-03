from django.core.exceptions import PermissionDenied
from .models import Center
from functools import wraps

def center_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, center_slug, *args, **kwargs):
        center = Center.objects.get(slug=center_slug)

        # Owner check
        if center.owner == request.user:
            return view_func(request, center_slug, *args, **kwargs)

        # Staff check
        if request.user.groups.filter(name='staff-staff').exists() and center.staff.filter(id=request.user.id).exists():
            return view_func(request, center_slug, *args, **kwargs)

        # Otherwise forbidden
        raise PermissionDenied

    return _wrapped_view