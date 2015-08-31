from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

from . import views

urlpatterns = [
    url(regex=r'^$', view=views.home, name='home'),
    url(r'^login/$', auth_views.login, name = 'loginpage'),
    url(r'^logout/$',auth_views.logout,{'template_name':'registration/logout.html'},name = 'logout'),
    url(r'^superhome/$', view = views.checkSuper, name = 'supercheck'),
    url(r'^cellcomp/$',view=views.playCellComp,name='play'),
    url(r'^newRating/$',view = views.addNewRating,name='rate'),
    url(r'^datadump/$',view=views.datadump,name = 'dump')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
