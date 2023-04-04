from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, PostEdit, PostDelete, ArticleCreate


urlpatterns = [
    path('', PostList.as_view(), name='posts_view'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/create', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit', PostEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]