from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, UserProfileForm
from .models import Post

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # optional; default is blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']         # newest first

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Set the author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Only allow the author of the post to edit.
        """
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')   # go back to list after deleting

    def test_func(self):
        """
        Only allow the author of the post to delete.
        """
        post = self.get_object()
        return post.author == self.request.user



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


