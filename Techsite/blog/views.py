from typing import Any
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class PostDraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(publish_date__isnull=True).order_by('-created_date')


## Publish Post ##

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)

## Comment part ##

@login_required  # type: ignore
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_deatil', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
