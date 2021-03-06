"""URLs module"""
from django.conf.urls.defaults import patterns, url

from social_auth.views import auth, complete, associate, associate_complete

try:
    from django.contrib.auth.signals import  user_logged_in
except:
    from .signals import login_register
    login_register()

urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'),
    url(r'^associate/(?P<backend>[^/]+)/$', associate, name='associate_begin'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
        name='associate_complete'),
)
