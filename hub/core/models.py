from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATES=(
    ('khrtoum', 'الخرطوم'),
    ('PortSudan', 'بورتسودان'),
    ('Kasala', 'كسلا'),

)
# Create your models here.

 

# center models
class Center(models.Model):

    title= models.CharField(max_length=200, verbose_name='اسم المركز')
    slug= models.SlugField(max_length=200, unique=True, allow_unicode=True)
    discription= models.TextField(verbose_name='وصف المركز')

    logo= models.ImageField(upload_to='centers/logos/%y/%m', blank=True, verbose_name='صورة الشعار')

    contact_phone= models.CharField(max_length=15, verbose_name='رقم التواصل')
    contact_email= models.EmailField(verbose_name='البريد الإلكتروني')
    website= models.URLField(blank=True, verbose_name='الموقع الإلكتروني')

    state= models.CharField(choices=STATES, verbose_name='الولاية')
    address= models.TextField(verbose_name='العنوان')
    latitude= models.FloatField(verbose_name=('خط الطول'))
    longitude= models.FloatField(verbose_name=('خط العرض'))

    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإنضمام')
    updated_at= models.DateField(auto_now=True, verbose_name='تاريخ التعديل')

    class Meta:
        verbose_name= 'المركز'
        verbose_name_plural= 'المراكز'
        ordering= ['-created_at']
    
    def __str__(self):
        return self.title

# user models
class Profile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', verbose_name='المستخدم')
    center= models.ForeignKey(Center, on_delete=models.SET_NULL, blank=True, null=True, related_name="users", verbose_name='المركز')
    job_title= models.CharField(max_length=100, verbose_name='المسمى الوظيفي')
    is_verified= models.BooleanField(default=False, verbose_name='معرف')
    
    class Meta:
        verbose_name='الملف الشخصي'
        verbose_name_plural='الملفات الشخصية'

    def __str__(self):
        return self.user
   

# course models
class Course(models.Model):

    title= models.CharField(max_length=200, verbose_name='اسم الدورة')
    slug= models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, null=True)
    center= models.ForeignKey(Center, on_delete=models.CASCADE, related_name='courses', verbose_name='المركز')

    image= models.ImageField(upload_to='courses/images/%y/%m', blank=True, verbose_name='اعلان الدورة')
    short_discription= models.CharField(max_length=300, verbose_name='وصف مختصر')
    learning_outcomes=models.TextField(verbose_name='مخرجات الدورة')
    details= models.TextField(verbose_name='التفاصيل')

    price= models.DecimalField(max_digits=6, decimal_places=4, verbose_name='السعر')
    currency= models.CharField(max_length=20, verbose_name='العملة')
    installment_available= models.BooleanField(default=False, verbose_name='يتوفر التقسيط')
    installment_details= models.TextField(verbose_name='تفاصيل التقسيط', blank=True)

    length= models.CharField(max_length=100, verbose_name='المدة')
    total_hours= models.PositiveIntegerField(verbose_name='عدد الساعات')

    start_date= models.DateField(verbose_name='تاريخ البدء', blank=True)
    schedule= models.TextField(verbose_name='الجدول الزمني', blank=True)

    TYPE= (
        ('in_person',''),
        ('onine',''),
        ('hybrid',''),
    )
    course_type= models.CharField(choices=TYPE, max_length=30, verbose_name='نوع الدورة')
    address= models.CharField(max_length=300, verbose_name='المكان', blank=True)
    online_platform= models.CharField(max_length=100, verbose_name='المنصة', blank=True)

    is_active= models.BooleanField(default=True, verbose_name='الدورة نشطة')
    is_featured= models.BooleanField(default=False, verbose_name='الدورة مميزة')

    view_count= models.PositiveIntegerField(verbose_name='عدد المشاهدات')
    leads_count= models.PositiveIntegerField(verbose_name='عدد المهتمين')

    created_by= models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='courses', verbose_name='المسؤول')
    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at= models.DateField(auto_now=True, verbose_name='تاريخ التعديل')

    class Meta:
        verbose_name= 'الدورة'
        verbose_name_plural= 'الدورات'
        ordering=['-created_at']

    def __str__(self):
        return f'{self.title}- {self.center.title}'


class Lead(models.Model):
    student_name= models.CharField(max_length=200, verbose_name='الاسم')
    student_phone= models.CharField(max_length=15, verbose_name='رقم التواصل')
    student_email= models.EmailField(blank=True, verbose_name='البريد الالكتروني')

    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='leads', verbose_name='الدورة')
    center= models.ForeignKey(Center, on_delete=models.CASCADE, related_name='leads', verbose_name='المركز')
    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name=''
        verbose_name_plural=''
        ordering=['-created_at']

    def __str__(self):
        return self.student_name
