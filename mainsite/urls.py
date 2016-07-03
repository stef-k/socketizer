from django.conf.urls import url
from django.views.generic import TemplateView
from mainsite import views

# Common URLs such as index, robots, etc

urlpatterns = [
    # robots.txt
    url(r'^robots\.txt$', TemplateView.as_view(template_name='util/robots.txt',
                                               content_type='text/plain'
                                               )),
    # site's landing page
    url(r'^$', views.index),
    url(r'^cmd/pool-info/$', views.pool_info),
]
