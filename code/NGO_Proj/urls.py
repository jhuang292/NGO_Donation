"""NGO_Proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import django
from django.contrib import admin
from django.urls import path
from ngo_app import views
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.urls import include
from django.contrib.auth.views import auth_login


Group.objects.get_or_create(name="User")
Group.objects.get_or_create(name="Admin")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ListAll.as_view()),
    #path('', views.HomeView.as_view()),

    path('user/update/<pk>', views.UpdateUsers.as_view()),
    path('user/del/<pk>' , views.DelUser.as_view()),
    path('user/add/', views.AddUser.as_view()),

    path('event/add/', views.AddEvent.as_view()),
    path(r'event/update/<pk>', views.UpdateEvent.as_view()),
    path(r'event/del/<pk>', views.DelEvent.as_view()),
    path(r'events/all', views.AllEventsView.as_view()),

    path('userdat/<first_name>', views.UpdateStuff.as_view()),
    path("login/", LoginView.as_view()),

    path('register/', views.EvenRegistrationView.as_view()),
    path('events/cart/', views.ListCArtView.as_view())

]


# from django.core.mail import send_mail
#
# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'polerbeardave@gmail.com',
#     ['david.r.dudek@gmail.com'],
#     fail_silently=False,
# )

