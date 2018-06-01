from django.conf.urls import url
from .views import post_list, post_detail

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^post/(?P<idx>\d+)/$', post_detail, name='post_detail'),
]
