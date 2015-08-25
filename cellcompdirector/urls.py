from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(regex=r'^$', view=views.home, name='home'),
    url(r'^login/$', auth_views.login, name = 'loginpage'),
    url(r'^cellcomp/$',view=views.playCellComp,name='play'),
    url(r'^newRating/$',view = views.addNewRating,name='rate')
]
