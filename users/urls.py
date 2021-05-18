from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>/', views.UserDetail.as_view(), name='user-details'),
    path('profile/', views.Profile.as_view(), name='user-profile'),
]
