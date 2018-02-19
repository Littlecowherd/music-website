from django.conf.urls import url
from . import views

app_name = 'music'
urlpatterns = [
    # ex: /music/
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^goodluck/$', views.good_luck, name='goodluck'),
]
