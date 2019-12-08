from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^join_game/$', views.join_game),
    url(r'^end_game/$', views.end_game),
    url(r'^start_game/$', views.start_game),
    url(r'', views.get_games),
]
