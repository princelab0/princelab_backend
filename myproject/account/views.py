from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from .forms import UserForm
from .models import User

from .serializers import UserSerializer, LoginSerializer
from .permissions import IsSuperUser
from .custom_throttling import CustomUserRateThrottle

from .utils import (
    get_number_of_hits,
    update_number_of_hits,
    check_user_has_credit_or_subscription,
    send_verification_email,
)

# Create your views here.


def home(request):
    return render(request, "index.html")


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect("user_profile")
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                email=email,
                password=password,
            )
            user.save()
            messages.success(request, "You have successfully create an account!!!")
            return redirect("home")
    else:
        form = UserForm()
    context = {
        "form": form,
    }
    return render(request, "account/register_user.html", context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect("user_profile")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email and Password!!!")
            return redirect("login")
    return render(request, "account/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You have logout!!!")
    return redirect("login")


@login_required(login_url="login")
def user_profile(request):
    # Get the Token associated with the currently logged-in user
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = None

    return render(request, "account/user_profile.html", {"token": token})


# API View Logic


class UserAPI(APIView):
    permission_classes = [IsSuperUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data["email"])
            # Send Verification email
            mail_subject = "Please activate your account"
            email_template = "account/email/account_verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            return Response(
                {"message": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response({"message": serializer.errors})

    def put(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors})

    def patch(self, request):
        data = request.data
        user = User.objects.get(id=data["id"])
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors})

    def delete(self, request):
        data = request.data
        user = User.objects.get(id=data["id"])
        user.delete()
        return Response({"message": "Person deleted"}, status=status.HTTP_200_OK)


class LoginAPI(APIView):
    permission_classes = [IsSuperUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        if User.objects.get(email=data["email"]).is_active == False:
            return Response(
                {
                    "message": "Your account is not activate please check your email to activate."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            email=serializer.data["email"], password=serializer.data["password"]
        )
        if not user:
            return Response(
                {"message": "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        user_data = {
            "id": user.id,
            "email": user.email,
        }
        return Response(
            {"message": "User Login", "Token": str(token), "user": user_data},
            status=status.HTTP_200_OK,
        )


class ServicesAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        # Get a specific query parameter named 'search' from the URL
        param_value = request.query_params.get("search")

        # Store the user that hit this API
        user = request.user

        if check_user_has_credit_or_subscription(user=user):
            return Response(
                {"message": "User does not have enough credit or a subscription."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the number of times this user has hit this API
        number_of_hits = get_number_of_hits(user)
        # Increment the number of hits
        number_of_hits += 1

        # Update the number of hits in the database
        update_number_of_hits(user, number_of_hits)

        if param_value is not None:
            return Response(
                {"message": f"Hello, {param_value}"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "No parameter provided"}, status=status.HTTP_200_OK
            )


@receiver(post_save, sender=ServicesAPI)
def post_save_print(sender, instance, created, **kwargs):
    print("API")
    if created:
        print("API Hits")


def activate(request, uidb64, token):
    # Activate the user by setting is_active true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Your account have been activated")
    else:
        return HttpResponse("Invalid activation link")
