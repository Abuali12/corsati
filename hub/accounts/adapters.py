from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import uuid

User= get_user_model()

class MyAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user= super().populate_user(request, sociallogin, data)

        if not user.username:
            username= data.get("given_name") or data.get("first_name")

            while User.objects.filter(username=username).exists():
                username = f"{username}_{uuid.uuid4().hex[:4]}"

        user.username = username

        return user
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        if not user.username:
            user.username = f"user_{user.id}"
            user.save()

        return user