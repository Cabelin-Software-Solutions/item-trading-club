from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^login/$', views.login_view, name='login'),
  url(r'^register/$', views.register_view, name='register'),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^profile/$', views.profile_view, name='profile'),
  url(r'^market/$', views.market_view, name='market'),
  url(r'^my_items/$', views.my_items_view, name='my_items'),
  url(r'^item/edit/$', views.item_edit_view, name='edit_item'),
  url(r'^item/delete/$', views.item_delete_view, name='delete_item'),
  url(r'^profile/edit/$', views.profile_edit_view, name='profile_edit'),
  url(r'^password/edit/$', views.password_edit_view, name='password_edit')
]
