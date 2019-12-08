from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^balance/$', views.get_balance),
    url(r'^ride_complete/$', views.ride_complete),
    url(r'^delivery_complete/$', views.delivery_complete),
    url(r'^leader_board/$', views.leaderboard),
    url(r'', views.user),
]
