"""jinrex URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^index/', include('app.urls')),
    url(r'^admin/', admin.site.urls),
]

# Добавьте URL соотношения, чтобы перенаправить запросы с корневового URL
# на URL приложения 
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/index/', permanent=True)),
    url(r'^index/blank/send_blank/index/$', RedirectView.as_view(url='/index/', permanent=True)),
    url(r'^catalog/', RedirectView.as_view(url='/index/', permanent=True)),
]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]