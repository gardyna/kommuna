from django.conf.urls import url

from . import views

app_name = 'bokhald'
urlpatterns = [
    url(r'^paymentsintimespan/$', views.payments_in_timespan, name='payments_in_timespan'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
