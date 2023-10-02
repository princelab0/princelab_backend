from django.shortcuts import render
from core.serializers import UserSerializers
from rest_framework import viewsets
from rest_framework import permissions
from core.models import AI_APP

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = AI_APP.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]