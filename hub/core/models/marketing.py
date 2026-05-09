from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class TrackingLink(models.Model):
    code = models.SlugField(unique=True)
    source_name = models.CharField(max_length=100)
    target_url = models.URLField()
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code

class RequestCourse(models.Model):
    REASON_CHOICES= {
        'not_found': 'لم أجد ما ابحث عنه',
        'too_expensive': 'السعر مرتفع',
        'wrong_time': 'وقت الدورة غير مناسب',
        'need_online': 'ارغب بدورةأونلاين',
        'need_offline': 'ارغب بدورة محلية',
        'not_enough_info': 'معلومات الدورة غير كافية',
        'other': 'أخرى',
    }
    course= models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الدورة')
    reason= models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name='السبب')
    searched= models.CharField(max_length=255, blank=True, null=True, verbose_name='سجل البحث')
    state= models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مكان الدورة')
    requested_course= models.CharField(max_length=255, blank=True, verbose_name='الدورة المطلوبة')
    message= models.TextField(blank=True, null=True, verbose_name='الرسالة')
    created_at= models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    def __str__(self):
        return f"طلب دورة: {self.requested_course} - السبب: {self.get_reason_display()}"
    
    class Meta:
        verbose_name = 'طلب دورة'
        verbose_name_plural = 'طلبات الدورات'
        ordering = ['-reason', '-created_at']