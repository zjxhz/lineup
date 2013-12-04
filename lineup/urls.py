from django.conf.urls import patterns, include, url
from django.contrib import admin
import lineup
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lineup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', lineup.views.wechat),
    url(r'^t/$', lineup.views.test),
)
