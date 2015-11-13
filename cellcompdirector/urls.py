from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings


from views.mainpages import *
from views.playfunctions import *

urlpatterns = [
    url(regex=r'^$', view=home, name='home'),
    url(r'^login/$', auth_views.login, name = 'loginpage'),
    url(r'^register/$', view=register, name='register'),
    url(r'^logout/$',auth_views.logout,{'template_name':'registration/logout.html'},name = 'logout'),
    url(r'^superhome/$', view = checkSuper, name = 'supercheck'),
    url(r'^cellcomp/$',view=playCellComp,name='play'),
    url(r'^cellcomp/newRating/$',view = addNewRating,name='rate'),
    url(r'^datadump/(?P<method>\w+)$',view=datadump,name = 'dump'),
    url(r'^sessionStart/$',view = sessionStart,name='newsession'),
    url(r'^passwordReset/$', view=resetPasswordRequest, name='resetrequest')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
