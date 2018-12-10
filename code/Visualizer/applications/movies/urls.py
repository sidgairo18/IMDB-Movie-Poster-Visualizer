from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^movies/p1', views.page1, name='page1'),
    url(r'^movies/p2', views.page2, name='page2'),
    url(r'^', views.index, name='index'),
]