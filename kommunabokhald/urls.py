from django.conf.urls import url

from . import views

app_name = 'bokhald'
urlpatterns = [
    url(r'^paymentsintimespan/$', views.payments_in_timespan, name='payments_in_timespan'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^groceries/$', views.grocery_list, name='groceries'),
    url(r'^addgrocery/$', views.add_grocery_item, name='add_grocery'),
    url(r'^removegrocery/(?P<id>[^/]+)/$', views.remove_grocery_item, name='remove_grocery'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
