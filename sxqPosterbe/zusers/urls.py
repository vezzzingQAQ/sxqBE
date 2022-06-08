from django.urls import path
from zusers import views

urlpatterns = [
    path('addStudent', views.addStudentView),
]
