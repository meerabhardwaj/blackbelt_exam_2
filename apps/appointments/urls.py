from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.appointments, name='appointments'),
    url(r'^/(?P<id>\d+)', views.show, name='show'),
    url(r'^add_new$', views.add_new, name='add_new'),
    url(r'^delete/(?P<id>\d+)', views.delete, name='delete'),
    url(r'^update/(?P<id>\d+)', views.update, name='update')

]
