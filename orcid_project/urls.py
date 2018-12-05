"""orcid_project URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include

from public_api import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url('admin/', admin.site.urls),

    # POST /auth/login/ (uses LDAP Backend for more details see the settings file)
    # login redirect url has been set to /rest/news/ in settings change it later according to needs
    # url('auth/', include('rest_framework.urls')),
    # url('rest/', include('rest.urls')),

]

# for Django debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns