# from django.shortcuts import get_list_or_404
# from django.shortcuts import render
from reviews.models import User
from rest_framework import viewsets
# from .permission import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
