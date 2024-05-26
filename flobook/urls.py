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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from onboarding.views import  signup, LoginView, logout_view, send_email, all_users_data, logout_view, getToken, BusinessLogoView
from manageaccounts.views import ManageAccounts



urlpatterns = [
   path('admin/', admin.site.urls),
     path('gettoken/', getToken, name='gettoken'),
   path('signup/', signup, name='signup'),


   path ('uploadlogo/', BusinessLogoView.as_view(), name='uploadlogo'),
#    path ('uploadlogo2/', upload_logo, name='uploadlogo'),
   

      path('login/', LoginView.as_view(), name='login'),
      path('logout/', logout_view, name='logout'),
     
#    path('ledger/', include('django_ledger.urls', namespace='django_ledger')),

   path('sendmail/', send_email, name='sendemail'),
   path('dashboardmetadata/', all_users_data, name='dashboard'),

    path('manageaccounts/', ManageAccounts.as_view(), name='manageaccounts'),
    #  path('manageaccounts/delete/<str:email>/', manageAccounts.as_view(), name='manageaccounts'),
#    path('uploadlogo/',PhotoView.as_view({'get': 'list', 'post': 'create'}), name='uploadlogo')

 
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
