from django.contrib import admin
from django.urls import path
from donor import views  # Import your views here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('donor/<int:volunteer_id>/', views.submit_donor, name='submit_donor'),  # Submit donor page
    path('report/', views.generate_report, name='generate_report'),  # Report generation
]
