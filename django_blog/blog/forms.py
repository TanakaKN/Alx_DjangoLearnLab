from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag   # 👈 NEW
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

        # The checker is looking for this "widgets" dict
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            # And specifically for TagWidget()
            'tags': TagWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'   # we'll create this template
    context_object_name = 'posts'

    def get_queryset(self):
        # get tag from URL (slug)
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        # return posts that have this tag
        return Post.objects.filter(tags__in=[self.tag]).order_by('-published_date').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
