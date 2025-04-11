"""proj_maths URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from MyEducationProject import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path("accounts/login/", auth_views.LoginView.as_view()),
    path('terms-list', views.terms_list),
    path('add-term', views.add_term),
    # path('send-term', views.send_term),
    path('stats', views.show_stats),
    # path('testing', views.testing),
    path('music_test', views.music_test),
    path('check_answer', views.check_test, name='check_answer'),
    path('admin/', admin.site.urls)
]
