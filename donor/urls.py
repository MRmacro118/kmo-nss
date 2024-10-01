from django.urls import path
from .views import home, submit_donor, generate_report, restricted_access

urlpatterns = [
    path('', home, name='home'),
    path('donor/<int:volunteer_id>/', submit_donor, name='submit_donor'),
    path('report/', generate_report, name='generate_report'),
    path('restricted/', restricted_access, name='restricted_access'),  # Add this line
]
