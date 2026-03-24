from django.db import models
from django.contrib.auth.models import User
from .centers import Center
from django.utils.text import slugify

class Course(models.Model):

    title= models.CharField(max_length=200, verbose_name='اسم الدورة')
    slug= models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, null=True)
    center= models.ForeignKey('Center', on_delete=models.CASCADE, related_name='courses', verbose_name='المركز')
    subjects= models.ManyToManyField('Subject', related_name='courses', verbose_name='مجالات الدورة')


    image= models.ImageField(upload_to='courses/images/%y/%m', blank=True, verbose_name='اعلان الدورة')
    short_discription= models.CharField(max_length=300, verbose_name='وصف مختصر')
    learning_outcomes=models.TextField(verbose_name='مخرجات الدورة')
    details= models.TextField(verbose_name='التفاصيل')

    CURRENCIES=(
        ('SDB','جنية سوداني'),
        ('USD','دولار أمريكي'),
        ('SR','ريال سعودي'),
        ('EGB','جنيه مصري'),
    )

    price= models.DecimalField(max_digits=20, decimal_places=2, verbose_name='السعر')
    currency= models.CharField(max_length=20, choices=CURRENCIES, verbose_name='العملة')
    installment_available= models.BooleanField(default=False, verbose_name='يتوفر التقسيط')
    installment_details= models.TextField(verbose_name='تفاصيل التقسيط', blank=True, null=True)

    length= models.CharField(max_length=100, verbose_name='المدة')

    TYPE= (
        ('in_person','حضوري'),
        ('online','أونلاين'),
        ('hybrid','حضوري وأونلاين'),
    )
    course_type= models.CharField(choices=TYPE, max_length=30, verbose_name='نوع الدورة')
    address= models.CharField(max_length=300, verbose_name='المكان', blank=True)
    online_platform= models.CharField(max_length=100, verbose_name='المنصة', blank=True)

    is_verified= models.BooleanField(default=False, verbose_name='الدورة معرفة')
    is_active= models.BooleanField(default=True, verbose_name='الدورة نشطة')
    is_featured= models.BooleanField(default=False, verbose_name='الدورة مميزة')

    view_count= models.PositiveIntegerField(blank=True, verbose_name='عدد المشاهدات', default=0)
    leads_count= models.PositiveIntegerField(blank=True, verbose_name='عدد المهتمين', default=0)

    created_by= models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='courses', verbose_name='المسؤول')
    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at= models.DateField(auto_now=True, verbose_name='تاريخ التعديل')

    class Meta:
        verbose_name= 'الدورة'
        verbose_name_plural= 'الدورات'
        ordering=['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1

            while Center.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}- {self.center.title}'

