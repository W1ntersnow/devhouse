from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    url(r'^auth/$', rest_framework_views.obtain_auth_token, name='auth'),

    # API views
    url(r'^api/shop/$', views.ShopCreate.as_view()),
    url(r'^api/schedule/(?P<shop_id>\d+)/$', views.ShopSchedule.as_view()),
    url(r'^api/schedule/update/(?P<shop_id>\d+)/$', views.UpdateSchedule.as_view()),
    url(r'^api/shop/(?P<shop_id>\d+)/$', views.ShopDetail.as_view()),
    url(r'^api/shop/close/$', views.ShopClose.as_view()),
    url(r'^api/user/$', views.UserCreate.as_view()),
    url(r'^api/user/(?P<user_id>\d+)/$', views.UserDetail.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


