from django.urls import path

from . import views
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url, include

from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cards', views.CardViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('updprefs/<str:bot_user_id>/', views.UpdPrefsApi.as_view(), name='apdprefs'),
    path('like/<str:bot_user_id>/', views.LikeApi.as_view(), name='like'),
    path('getcards/<str:bot_user_id>/', views.GetCardsApi.as_view(), name='getcards'),
    path('register/<str:bot_user_id>/', views.RegisterUser.as_view(), name='adduser'),
    path('getmycats/<str:bot_user_id>/', views.GetStrCategories.as_view(), name='getmycats'),


]



