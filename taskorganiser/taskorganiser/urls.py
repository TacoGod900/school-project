"""
URL configuration for taskorganiser project.

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
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # mount the boards app at the site root
    path('', include('boards.urls')),
]
=======
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main.views import dashboard_view, home_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> c351e6fa5d255e2faf3413dfa7e2098f2bf0dc52
