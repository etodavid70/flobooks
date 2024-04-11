"""
URL configuration for flobook project.

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
from django.contrib import admin
from django.urls import path
from onboarding.views import CustomUserListCreate, CustomUserRetrieveUpdateDestroy, GetUserByEmail, GetUserByEmail2, signup

urlpatterns = [
   path('admin/', admin.site.urls),

   path('signup/', signup, name='signup'),
    path('users/', CustomUserListCreate.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroy.as_view(), name='user-detail'),

    #django method to get user by email
    path('user/<str:email>/', GetUserByEmail.as_view(),  name='get-user-by-email'),

    #django rest method
    path('users/<str:email>/', GetUserByEmail2.as_view(), name='get-user-by-email'),
]
