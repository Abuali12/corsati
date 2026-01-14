from django.urls import path
from . import views

urlpatterns = [
    path('', views.centers, name='centers'),
    path('center/<int:center_id>', views.center, name='center'),
]