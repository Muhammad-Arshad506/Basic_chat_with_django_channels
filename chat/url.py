from django.urls import path
from .consumers import ChatConsumer, GroupConsumer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("token/", obtain_auth_token)

]

websocket_urlpatterns = [
    path('ws/', ChatConsumer.as_asgi()),
    path('ws/group/', GroupConsumer.as_asgi()),

]
