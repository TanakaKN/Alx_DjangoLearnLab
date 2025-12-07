
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, UserProfileForm

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Comment
from .forms import PostForm, CommentForm

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
    template_name = 'blog/post_detail.html'  # or whatever you used

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # should already exist

    def form_valid(self, form):
        # Set the author to the logged-in user
        form.instance.author = self.request.user
        # You might be setting published_date somewhere else; if needed,
        # you can import timezone and set it here.
        response = super().form_valid(form)
        # Handle tags after the Post is saved
        self._save_tags(form)
        return response

    def _save_tags(self, form):
        tags_str = form.cleaned_data.get('tags', '')
        if not tags_str:
            return
        tags_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        for name in tags_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            self.object.tags.add(tag_obj)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the tags field with current tags
        initial['tags'] = ', '.join(t.name for t in self.object.tags.all())
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        # Clear old tags and set new ones
        self.object.tags.clear()
        self._save_tags(form)
        return response

    def _save_tags(self, form):
        tags_str = form.cleaned_data.get('tags', '')
        if not tags_str:
            return
        tags_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        for name in tags_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            self.object.tags.add(tag_obj)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


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
    
def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).order_by('-published_date')
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')

    context = {
        'query': query,
        'posts': posts,
    }
    return render(request, 'blog/search_results.html', context)




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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user



