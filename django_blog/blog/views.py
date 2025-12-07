from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .models import Post
from .forms import RegisterForm

def home(request):
    return render(request, "blog/home.html")

def post_list(request):
    posts = Post.objects.all().order_by("-published_date")
    return render(request, "blog/posts.html", {"posts": posts})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

class BlogLoginView(LoginView):
    template_name = "blog/login.html"
class BlogLogoutView(LogoutView):
    next_page = "home"
