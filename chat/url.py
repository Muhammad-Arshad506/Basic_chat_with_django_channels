from django.urls import path
from .consumers import ChatConsumer, GroupConsumer
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserView
urlpatterns = [
    path("token/", obtain_auth_token),
    path("user/", UserView.as_view())

]

websocket_urlpatterns = [
    path('ws/', ChatConsumer.as_asgi()),
    path('ws/group/', GroupConsumer.as_asgi()),

]
