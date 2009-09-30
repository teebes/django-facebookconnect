from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('facebookconnect.views',
        url(r'^xd_receiver\.htm$', direct_to_template, {'template': 'xd_receiver.htm'}, name='xd_receiver'),
        url(r'^login_facebook_connect/$', 'login_facebook_connect', name='facebook_connect_ajax'),
    )

