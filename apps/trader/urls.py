from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^login/$', views.login_view, name='login'),
  url(r'^register/$', views.register_view, name='register'),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^profile/$', views.profile_view, name='profile'),
  url(r'^market/$', views.market_view, name='market'),
  url(r'^trades/$', views.trade_view, name='trades'),
  url(r'^my_items/$', views.my_items_view, name='my_items'),
  url(r'^item/edit/$', views.item_edit_view, name='edit_item'),
  url(r'^item/delete/$', views.item_delete_view, name='delete_item'),
  url(r'^item/trade/request$', views.trade_request_view, name='trade_request'),
  url(r'^item/trade/(?P<trade_id>\d+)/window$', views.trade_window_view, name='trade_window'),
  url(r'^item/trade/(?P<trade_id>\d+)/update$', views.trade_update_view, name='trade_update'),
  url(r'^item/trade/(?P<trade_id>\d+)/finalize$', views.trade_finalize_view, name='trade_finalize'),
  url(r'^item/trade/(?P<trade_id>\d+)/cancel$', views.trade_cancel_view, name='trade_cancel'),
  url(r'^item/trade/(?P<trade_id>\d+)/accept$', views.trade_accept_view, name='trade_accept'),
  url(r'^item/trade/(?P<trade_id>\d+)/reject$', views.trade_reject_view, name='trade_reject'),
  url(r'^profile/edit/$', views.profile_edit_view, name='profile_edit'),
  url(r'^password/edit/$', views.password_edit_view, name='password_edit')
]
