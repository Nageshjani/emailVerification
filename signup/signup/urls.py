"""signup URL Configuration

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
from django.contrib import admin
from django.urls import path
from myapp.views import signupView,verify_email,signup_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signupView,name='signup'),
    path('verify_email/<str:username>/<str:token>/', verify_email, name='verify_email'),
    path('signup_success/', signup_success, name='signup_success'),


]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.signup_view, name='signup'),
#     path('verify_email_sent/', views.verify_email_sent, name='verify_email_sent'),
#     path('verify_email/<str:username>/<str:token>/', views.verify_email, name='verify_email'),
#     path('signup_success/', views.signup_success, name='signup_success'),
# ]
