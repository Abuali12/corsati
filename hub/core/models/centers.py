from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Center(models.Model):

    title= models.CharField(max_length=200, verbose_name='اسم المركز')
    slug= models.SlugField(max_length=200, unique=True, allow_unicode=True)

    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_centers', null=True)
    staff= models.ManyToManyField(User, blank=True, related_name='working_centers')

    discription= models.TextField(verbose_name='وصف المركز')
    subjects= models.ManyToManyField('Subject', related_name='centers', verbose_name='مجالات المركز')

    is_verified= models.BooleanField(default=False, verbose_name='معرف')
    is_individual= models.BooleanField(default=False, verbose_name='فردي')
    is_deleted= models.BooleanField(default=False, verbose_name='محذوف')
    is_active= models.BooleanField(default=True, verbose_name='نشط')
    is_featured= models.BooleanField(default=False, verbose_name='مميز')

    TYPE= (
        ('in_person','حضوري'),
        ('online','عن بعد'),
        ('hybrid','حضوري وعن بعد'),
    )
    center_type= models.CharField(choices=TYPE,default=
                                  'in_person', max_length=30, verbose_name='نوع المركز')

    logo= models.ImageField(upload_to='centers/logos/%y/%m', blank=True, null=True , verbose_name='صورة الشعار')
    logo_url= models.URLField(blank=True, null=True, verbose_name='رابط الشعار')
    contact_phone= models.CharField(max_length=15, verbose_name='رقم التواصل', blank=True, null=True)
    contact_email= models.EmailField(verbose_name='البريد الإلكتروني')
    website= models.URLField(blank=True, null=True, verbose_name='الموقع الإلكتروني')

    state= models.ForeignKey('State', on_delete=models.PROTECT, related_name='centers', verbose_name='الولاية', blank=True, null=True)
    address= models.TextField(verbose_name='العنوان', blank=True, null=True)
    latitude= models.FloatField(verbose_name=('خط الطول'), blank=True, null=True)
    longitude= models.FloatField(verbose_name=('خط العرض'), blank=True, null=True)

    view_count= models.PositiveIntegerField(blank=True, verbose_name='عدد المشاهدات', default=0)

    created_at= models.DateField(auto_now_add=True, verbose_name='تاريخ الإنضمام')
    updated_at= models.DateField(auto_now=True, verbose_name='تاريخ التعديل')

    class Meta:
        verbose_name= 'المركز'
        verbose_name_plural= 'المراكز'
        ordering= ['-created_at']

        permissions = [
            ('can_access_dashboard', 'can_access_dashboard'),
        ]

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
        return self.title
