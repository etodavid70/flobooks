from django.urls import path
from .views import subuser_login, subuser_logout

urlpatterns = [
    path('login/', subuser_login, name='subuser-login'),
     path('logout/', subuser_logout, name='subuser_logout'),
    # other paths...
]
