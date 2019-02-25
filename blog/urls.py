"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
import xadmin
from django.conf.urls import *
from blog.settings import STATIC_ROOT, MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path('^media/(?P<path>.*)$', serve, {
        'document_root': MEDIA_ROOT,
    }),
    re_path('^static/(?P<path>.*)$', serve, {
        'document_root': STATIC_ROOT,
    }),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include(('apps.MainCoreApp.urls', 'blog'), namespace='blog')),
]


handler400 = 'apps.MainCoreApp.views.page400'
handler403 = 'apps.MainCoreApp.views.page403'
handler500 = 'apps.MainCoreApp.views.page500'