# Create your views here.
import json

from django.db.models import Q
from django.shortcuts import render
from .serialzer import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user:
            username = request.user.username
            user_list = get_user_model().objects.all().\
                exclude(username=username).order_by("username")
            result = UserSerializer(user_list,many=True).data
            return Response(result)

