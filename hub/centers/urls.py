from django.urls import path
from . import views

urlpatterns = [
    path('', views.centers, name='centers'),
    path('center/<str:center_slug>', views.center, name='center'),
    path('center_dashboard/<str:center_slug>', views.center_dashboard, name='center_dashboard'),
    path('add_center', views.add_center, name='add_center'),
    path('edit_center/<str:center_slug>', views.edit_center, name='edit_center'),
    path('delete_center/<str:center_slug>', views.delete_center, name='delete_center'),
    path('clear/', views.clear, name='clear_center'),
]