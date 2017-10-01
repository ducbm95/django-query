from django.conf.urls import include, url
from django.contrib import admin

import welcome.views
import queries.views
import categories.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', queries.views.index),
    url(r'^health$', welcome.views.health),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^queries$', queries.views.index, name='query_page'),
    url(r'^categories/$', categories.views.index, name='list_main_category'),
    url(r'^categories/(?P<category_id>[0-9]*)$', categories.views.show, name='list_sub_category')
]
