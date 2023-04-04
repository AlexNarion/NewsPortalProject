from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .filters import PostFilter
from .forms import PostFilterForm, PostForm


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

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'newsedit.html'
