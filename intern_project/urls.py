"""intern_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views as webapp_views
from doctype import views as doctype_views
from docdata import views as docdata_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', doctype_views.home),
    path('trial/', doctype_views.trial),
    path('upload/', doctype_views.upload),
    path('doctype/', doctype_views.doctype),
    path('rawdata/', docdata_views.RawDataDisplay.as_view()),
    path('processeddata/', docdata_views.ProcessedDataDisplay.as_view()),
    path('employee/', webapp_views.employeeList.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)