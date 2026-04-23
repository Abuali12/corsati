from django.core.exceptions import PermissionDenied
from .models import Center
from functools import wraps

from supabase import create_client
from hub import settings
import uuid

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


def upload_to_supabase(file, folder= 'uploads'):
    supabase= create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    print(type(supabase))
    file_ext= file.name.split('.')[-1]
    file_name= f"{folder}/{uuid.uuid4()}.{file_ext}"
    response = (
        supabase.storage
        .from_("corsati-imgs")
        .upload(
            file_name,
            file.read(),
            file_options={"cache-control": "3600", "upsert": "false"}
        )
    )
    
    public_url= supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)

    return public_url