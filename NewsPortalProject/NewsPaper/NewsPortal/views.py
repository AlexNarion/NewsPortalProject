import logging
from urllib import request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin


from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostFilterForm, PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = 'addtime'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)
class PostDetail(CustomSuccessMessageMixin, DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан!'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk':self.get_object().id})


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.post = self.get_object()
        self.object.save()
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.post_author.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.test_func()
        return context


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
        author = get_object_or_404(Author, username=self.request.user)
        post.post_author = author
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
        author = get_object_or_404(Author, username=self.request.user)
        post.post_author = author
        return super().form_valid(form)

    permission_required = ('NewsPortal.add_post',)

class CategoryListView(ListView):
    model = Post
    template_name = 'categorylist.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-addtime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category':category, 'message':message})


class AuthorListView(ListView):
    model = Post
    template_name = 'author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        self.post_author = get_object_or_404(Author, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_author=self.post_author).order_by('-rating')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_not_subscriber'] = self.request.user not in self.post_author.subscribers.all()
        context['user_is_subscriber'] = self.request.user in self.post_author.subscribers.all()
        context['author'] = self.post_author
        return context

def authorsub(request, pk):
    user = request.user
    post_author = Author.objects.get(id=pk)
    post_author.subscribers.add(user)

    message = 'Вы подписались на автора!'
    return render(request, 'authorsub.html', {'post_author': post_author, 'message': message})


def author_un_sub(request, pk):
    user = request.user
    post_author = Author.objects.get(id=pk)
    post_author.subscribers.remove(user)

    message = 'Вы отписались от автора'
    return render(request, 'authorunsub.html', {'post_author': post_author, 'message': message})


def category_un_sub(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписались от категории'
    return render(request, 'categoryunsub.html', {'category': category, 'message': message})


