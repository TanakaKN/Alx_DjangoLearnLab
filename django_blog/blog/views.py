from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, UserProfileForm
from .models import Post


# Home page (already had something like this)
def home(request):
    return render(request, "blog/home.html")


class UserLoginView(LoginView):
    template_name = "blog/login.html"

def post_list(request):
    """Simple page that will list all blog posts."""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})    


class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()       # creates the user in DB
            login(request, user)     # automatically log in
            return redirect("home")  # go to home after register
    else:
        form = UserRegistrationForm()

    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")    # reload profile page
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "blog/profile.html", {"form": form})


