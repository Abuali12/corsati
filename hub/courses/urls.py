from django.urls import path
from . import views

urlpatterns= [
    path('', views.courses, name='courses'),
    path('course/<str:course_slug>', views.course, name='course'),
    path('course_lead/<str:course_slug>', views.course_lead, name= 'course_lead'),
    path('add_course/<str:center_slug>', views.add_course, name='add_course'),
    path('edit_course/<str:course_slug>', views.edit_course, name='edit_course'),
    path('delete_course/<str:course_slug>', views.delete_course, name='delete_course'),
    path('deactivate_course/<str:course_slug>', views.deactivate, name= 'deactivate_course'),
    path('clear/', views.clear, name='clear_course'),    
]