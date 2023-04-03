from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter
from .forms import PostFilterForm


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
        filterset_kwargs = self.get_filterset_kwargs()
        filterset_kwargs['form'] = PostFilterForm(data=filterset_kwargs['data'], queryset=filterset_kwargs['queryset'])
        return self.filterset_class(**filterset_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.get_filterset()
        return context