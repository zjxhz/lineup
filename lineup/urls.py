from django.conf.urls import patterns, include, url
from django.contrib import admin
from lineup.views import WaiterAdminView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lineup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lineup.views.wechat'),
    url(r'^t/$', 'lineup.views.test'),
    url(r'^line/admin/$', WaiterAdminView.as_view()),
    url(r'^line/(?P<line_id>\d+)/next/avaliable$', 'lineup.views.next_user_avaliable', name='next_abaliable'),
    url(r'^line/(?P<line_id>\d+)/next/get$', 'lineup.views.get_next_no', name='get_next_no'),
)
