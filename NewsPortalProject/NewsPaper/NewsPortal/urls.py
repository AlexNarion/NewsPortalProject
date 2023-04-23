from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, PostEdit, PostDelete, ArticleCreate, CategoryListView, subscribe, AuthorListView, authorsub, author_un_sub
from .views import category_un_sub
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*10)(PostList.as_view()), name='posts_view'),
    path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/create', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit', PostEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/susbcribe',subscribe, name='subscribe'),
    path('author/<int:pk>', AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/authorsub',authorsub, name='author_subscribe'),
    path('author/<int:pk>/author_un_sub',author_un_sub, name='author_un_sub'),
    path('categories/<int:pk>/un_sub',category_un_sub,name='category_un_sub' )
]