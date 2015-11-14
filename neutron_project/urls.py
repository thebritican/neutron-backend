"""neutron_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import re

from django.conf import settings
from django.conf.urls import include, url
from django.views.static import serve
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from graphene.contrib.django.views import GraphQLView
from neutron.schema import schema

# Hack for allow static files in prod (Heroku/Dokku)
def static(prefix, view=serve, **kwargs):
    return [
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('neutron.urls')),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
    url(r'^graphiql', include('django_graphiql.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
