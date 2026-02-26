"""
URL configuration for Insight project.

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
from django.urls import path,include
from myapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('feature/', views.feature, name = 'feature'),
    path('project/', views.project, name = 'project'),
    path('service/', views.service, name = 'service'),
    path('team/', views.team, name = 'team'),
    path('testimonial/', views.testimonial, name = 'testimonial'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('fpass/', views.fpass, name = 'fpass'),
    path('otp/', views.otp, name = 'otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout, name='logout'),
    path('newpass/', views.newpass, name='newpass'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('changepass/', views.changepass, name='changepass'),
    path('add_design/', views.add_design, name='add_design'),
    path('manage_design/',views.manage_design, name='manage_design'),
    path('edit_design/<int:pk>/',views.edit_design, name='edit_design'),
    path('delete_design/<int:pk>/',views.delete_design, name='delete_design'),
    path('home/',views.home, name='home'),
    path('design_info/<slug:design_slug>/',views.design_info, name='design_info'),
    path('moodboard_add/<int:pk>/',views.moodboard_add,name='moodboard_add'),
    path('moodboard/',views.moodboard,name='moodboard'),
    path('designer_info/',views.designer_info,name='designer_info'),
    ]
