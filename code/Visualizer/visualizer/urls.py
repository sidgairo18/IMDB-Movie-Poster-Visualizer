from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^movies/', include('applications.movies.urls')),
    url(r'^admin/', admin.site.urls),
]