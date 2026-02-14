from django.urls import path
from . import views

urlpatterns= [
    path('', views.courses, name='courses'),
    path('course/<slug:course_slug>', views.course, name='course'),
    path('add_course/<slug:center_slug>', views.add_course, name='add_course'),
    path('edit_course/<slug:course_slug>', views.edit_course, name='edit_course'),
    path('delete_course/<slug:course_slug>', views.delete_course, name='delete_course'),
    path('clear/', views.clear, name='clear_course'),    
]