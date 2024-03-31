"""
URL configuration for django_project_chuhonin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import signup
from django.contrib import admin
from django.urls import path, include

from hotels import views

urlpatterns = [
    path("guests/register/", views.register, name="register"),
    path("guests/profile/", views.profile, name="register"),
    path("guests/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', views.index, name='отели'),
    path('hotel/<str:hotel_path>/', views.rooms, name='номера'),
    path('agreements', views.agreements, name='бронь'),
    # path('profile', views.profile, name='профиль'),
    path('review', views.review, name='отзывы'),
    path('report', views.report, name='постояльцы'),
]
