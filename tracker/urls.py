# api/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskList.as_view(), name='task-list'),
    path('<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('<int:pk>/pause', views.TaskPause.as_view(), name='task-pause'),
    path('<int:pk>/resume', views.TaskResume.as_view(), name='task-resume'),
    path('<int:pk>/finish', views.TaskFinish.as_view(), name='task-finish'),
    path('email', views.SendEmailView.as_view(), name='email'),
    path('report', views.TaskReportView.as_view(), name='report'),
    path('monitor', views.CeleryMonitor.as_view(), name='monitor'),
]
