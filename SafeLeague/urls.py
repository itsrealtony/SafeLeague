"""
URL configuration for SafeLeague project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.benvenuto, name='benvenuto'),
    path('principale/', views.principale, name='principale'),
    path('login_responsabile/', views.login_responsabile, name='login_responsabile'),
    path('login_arbitro/', views.login_arbitro, name='login_arbitro'),
    path('login_dirigente/', views.login_dirigente, name='login_dirigente'),
    path('principale_responsabile/', views.principale_responsabile, name='principale_responsabile'),
    path('principale_arbitro/', views.principale_arbitro, name='principale_arbitro'),
    path('principale_dirigente/', views.principale_dirigente, name='principale_dirigente'),
]
