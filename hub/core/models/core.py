from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Subject(models.Model):
    title= models.CharField(max_length=100, verbose_name='اسم المجال', unique=True)
    class Meta:
        verbose_name= 'المجال'
        verbose_name_plural= 'المجالات'
        ordering=['title']
    def __str__(self):
        return self.title

class State(models.Model):
    title= models.CharField(max_length=100, verbose_name='اسم الولاية', unique=True)

    class Meta:
        verbose_name= 'الولاية'
        verbose_name_plural= 'الولايات'
        ordering=['title']
    def __str__(self):
        return self.title
    

class Lead(models.Model):
    student_name= models.CharField(max_length=200, verbose_name='الاسم')
    student_phone= models.CharField(max_length=30, verbose_name='رقم الهاتف', blank= True, null=True)
    student_email= models.EmailField(verbose_name='البريد الالكتروني', blank=True, null= True)
    note= models.TextField(verbose_name='تعليق', blank=True, null=True)
    course= models.ForeignKey('Course', on_delete=models.PROTECT, related_name='leads', verbose_name='الدورة')
    center= models.ForeignKey('Center', on_delete=models.PROTECT, related_name='leads', verbose_name='المركز')
    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    TYPE_CHOICES = [
        ('course', 'Course Enrollment'),
        ('center', 'General Center Contact'),
    ]
    lead_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='course')
    class Meta:
        verbose_name='الدليل'
        verbose_name_plural='الأدلة'
        ordering=['-created_at']

    def __str__(self):
        return self.student_name


