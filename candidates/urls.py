from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('candidate_list/', views.candidates_list, name='candidates_list'),
    path('create/', views.create_candidate, name='create_candidate'),
    path('delete/<int:pk>/', views.delete_candidate, name='delete_candidate'),
    path('edit/<int:pk>/', views.edit_candidate, name='edit_candidate'),
    path('', views.signup_student, name='signup_student'),
    path('signup/recruiter/', views.signup_recruiter, name='signup_recruiter'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.userLogout, name='logout'),
]