from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_cash/$', views.add_cash),
    url(r'', views.get_all_transaction),
]
