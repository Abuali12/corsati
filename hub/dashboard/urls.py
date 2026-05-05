from django.urls import path
from . import views

urlpatterns = [    
    path('centers_dashboard',views.centers_dashboard, name= 'centers_dashboard'),
    path('center_dashboard/<str:center_slug>', views.center_dashboard, name='center_dashboard'),
    path('leads/<str:center_slug>', views.leads, name='leads'),
    path('clear_leads/<str:center_slug>/', views.lead_clear, name='lead_clear'),
    path('contacted_lead/<int:id>', views.contacted_lead, name='contacted_lead'),
    path('closed_lead/<int:id>', views.closed_lead, name='closed_lead')
]