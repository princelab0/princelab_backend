from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from .models import User

# Create your views here.


def home(request):
    return render(request, "index.html")


def register_user(request):
    if request.method == "POST":
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
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
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
    return render(request, "account/user_profile.html")
