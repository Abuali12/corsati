from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
        
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', verbose_name='المستخدم')
    center= models.ForeignKey('Center', on_delete=models.SET_NULL, blank=True, null=True, related_name="users", verbose_name='المركز')
    
    class Meta:
        verbose_name='الملف الشخصي'
        verbose_name_plural='الملفات الشخصية'

    def __str__(self):
        return self.user.username
   
