import os

from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings

from feedservice.webservice.views import ParseView, IndexView


urlpatterns = patterns('',
    (r'^$',               IndexView.as_view()),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^parse$',          ParseView.as_view()),
)
