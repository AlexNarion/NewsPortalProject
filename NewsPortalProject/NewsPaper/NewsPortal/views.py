import logging

from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostFilterForm, PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = 'addtime'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(FilterView):
    model = Post
    ordering = 'addtime'
    template_name = 'postsearch.html'
    context_object_name = 'post_search'
    paginate_by = 10
    filterset_class = PostFilter

    def get_filterset(self, filterset_class):
        filterset_kwargs = self.get_filterset_kwargs(filterset_class)
        return filterset_class(**filterset_kwargs)


    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs


class NewsCreate(CreateView,PermissionRequiredMixin, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'

    permission_required = ['add_post']


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choose = 'NY'
        return super().form_valid(form)




class PostEdit(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'
    permission_required = ['change_post']



class PostDelete(DeleteView):
    model = Post
    template_name = 'postdelete.html'
    success_url = reverse_lazy('posts_view')


class ArticleCreate(CreateView, LoginRequiredMixin,PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choose = 'AR'
        return super().form_valid(form)

    permission_required = ['add_post']