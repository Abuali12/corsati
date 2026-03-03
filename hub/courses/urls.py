from django.urls import path
from . import views

urlpatterns= [
    path('', views.courses, name='courses'),
    path('course/<int:course_id>', views.course, name='course'),
    path('add_course/<slug:center_slug>', views.add_course, name='add_course'),
    path('edit_course/<int:course_id>', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('clear/', views.clear, name='clear_course'),    
]