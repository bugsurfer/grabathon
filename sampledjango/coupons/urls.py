from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_coupon/$', views.create_coupon),
    url(r'^user_coupon/$', views.user_coupons),
    url(r'^redeem_coupon/$', views.reedem_coupon),
    url(r'', views.get_coupons),
]
