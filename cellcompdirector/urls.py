from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'^$', view=views.home, name='home'),
    url(regex=r'^start/(?P<username>\w+)$', view=views.start, name='userset'),
]
