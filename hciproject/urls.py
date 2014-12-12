from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bwf.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hciproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home$', home, name='home'),
    url(r'^bill/new$', add_bill, name='add_bill'),
    url(r'^friend/new$', add_friend, name='add_friend'),

    url(r'^friend/(?P<pk>\d+)$', bill_list, name='bill_list'),


    url(r'^signup$', SignupView.as_view()  ),
    url(r'^login$', 'django.contrib.auth.views.login' ),
    url(r'^logout$', 'django.contrib.auth.views.logout' ),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
