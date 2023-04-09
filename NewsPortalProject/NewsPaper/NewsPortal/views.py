import logging

from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Subscribers, Category
from .filters import PostFilter, CategoryFilter
from .forms import PostFilterForm, PostForm, CategoryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


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


class NewsCreate(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'

    permission_required = ('NewsPortal.add_post',)


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choose = 'NY'
        return super().form_valid(form)




class PostEdit(PermissionRequiredMixin,UpdateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'
    permission_required = ('NewsPortal.change_post',)



class PostDelete(DeleteView):
    model = Post
    template_name = 'postdelete.html'
    success_url = reverse_lazy('posts_view')
    permission_required = ('NewsPortal.delete_post',)


class ArticleCreate(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choose = 'AR'
        return super().form_valid(form)

    permission_required = ('NewsPortal.add_post',)

@csrf_exempt
def get_subscriber(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            user = request.user
            category = form.cleaned_data['category']
            subscriber, created = Subscribers.objects.get_or_create(user=user, category=category)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Подписка успешно создана'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Вы уже подписаны на эту категорию'})
    else:
        form = CategoryForm()
        posts = Post.objects.all()
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {'posts': posts, 'form': form, 'page_obj': page_obj}