from django.contrib import admin
from .models import Center, Course, Lead, Profile

# Register your models here.
admin.site.register(Center)
admin.site.register(Course)
admin.site.register(Lead)
admin.site.register(Profile)