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
from django.conf.urls import url

from public_api import views

urlpatterns = [
    url('redirect', views.uri_redirect, name='redirect'),

    url('invitation_link/(?P<token>[0-9A-Za-z]{1,32})', views.invitation_link_view,
        name='invitation_link'),

    url('contact', views.contact, name='contact'),

    url('orcid_create_or_linking_rejected', views.reject_orcid_creation_and_linking, name='user_reject_orcid'),

    url('faq_english', views.faq_english, name='faq-en'),

    url('faq_german', views.faq_german, name='faq-de'),

]