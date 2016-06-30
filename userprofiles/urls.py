from django.conf.urls import url
from userprofiles import views

urlpatterns = [
    url(r'^profile/$', views.UserProfile.as_view(), name='profile'),
    url(r'^domain/new/$', views.DomainCreate.as_view(), name='domain-add'),
    url(r'^domain/(?P<pk>[0-9]+)/$', views.DomainUpdate.as_view(),
        name='domain-update'),
    url(r'^domain/(?P<pk>[0-9]+)/regenerate-key$',
        views.regenerate_api_key,
        name='domain-regenerate-key'),
    url(r'^domain/(?P<pk>[0-9]+)/delete/$', views.domain_delete,
        name='domain-delete'),
]
