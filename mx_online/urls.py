"""mx_online URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from apps.users.views import LoginView, LogoutView, SendSmsView, image_sms, RegisterView
from apps.organizations.views import OrgView
from mx_online.settings import MEDIA_ROOT

import xadmin

urlpatterns = [
    # assign url for all uploaded files
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('captcha/', include('captcha.urls')),
    path('send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),  # cancel csrf token check
    path('register/', RegisterView.as_view(), name='register'),
    path('sms_code/code/', image_sms),

    # organization related pages
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),

    # operations related pages
    url(r'^ope/', include(('apps.operations.urls', 'operations'), namespace='ope')),

    # course related pages
    url(r'^courses/', include(('apps.courses.urls', 'course'), namespace='courses')),
]
