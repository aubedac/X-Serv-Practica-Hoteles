"""PracticaFinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', 'hoteles.views.homepage'),
    url(r'^alojamientos$', 'hoteles.views.accommodations'),
    url(r'^alojamientos/(\d+)', 'hoteles.views.hotelView'),
    url(r'^register/$', 'hoteles.views.register'),
    url(r'^login/$','hoteles.views.authentication'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^about$', 'hoteles.views.about'),
    url(r'^(.*)/xml$', 'hoteles.views.userXml'),
    url(r'^admin/', admin.site.urls),
    #url(r'^css/(style.css)$','django.views.static.serve',
    #    {'document_root':'templates/templateCss/css/'}),
    url(r'^css/style.css$','hoteles.views.css'),
    url(r'^images/(.*)$','django.views.static.serve',
        {'document_root':'templates/templateCss/images/'}),
    url(r'^js/(.*)$', 'django.views.static.serve',
        {'document_root':'templates/templateCss/js/'}),
    #url(r'^alojamientos/css/(style.css)$', 'django.views.static.serve',
    #    {'document_root':'templates/templateCss/css/'}),
    url(r'^alojamientos/css/style.css$', 'hoteles.views.css'),
    url(r'^alojamientos/images/(.*)$','django.views.static.serve',
        {'document_root':'templates/templateCss/images/'}),
    url(r'^alojamientos/js/(.*)$', 'django.views.static.serve',
        {'document_root':'templates/templateCss/js/'}),
    url(r'^fonts/(.*)$', 'django.views.static.serve',
        {'document_root' : 'templates/templateCss/fonts/'}),
    url(r'^alojamientos/fonts/(.*)$', 'django.views.static.serve',
        {'document_root' : 'templates/templateCss/fonts/'}),
    url(r'^(.*)$', 'hoteles.views.userpage'),
]
