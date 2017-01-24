from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/(?P<type_id>[\w\.\d]+)', views.detail, name='detail'),
]
