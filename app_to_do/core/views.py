'''
from django.shortcuts import render

# Create your views here.import the listApiView from rest_framework.generics.
from rest_framework.generics import ListAPIView
from core.models import User #import user model from the models.py.
from app_to_do.serializer import UserSerializator
#import the serializer class from app to do module. 

#create a class that inherits from ListAPIView, which is a generic view provided by Django REST framework for displaying lists of objects.
def UserListView(ListAPIView):
    querysets=User.objects.all()
    serializer_class=UserSerializator

#create a variable that retrives all the values from the model Users.


from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from app_to_do.serializers import UserSerializator,SignInSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializator
    permission_classes = [permissions.IsAuthenticated]

class SignInView(APIView):
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Authentication successful
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid input data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
from django.shortcuts import get_object_or_404
from core.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from app_to_do.serializers import  SignInSerializer
from rest_framework.response import Response
from django.shortcuts import render,redirect

class SignInView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer =  SignInSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer =  SignInSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        
