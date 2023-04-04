from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate


urlpatterns = [
    path('', PostList.as_view(), name='posts_view'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create', NewsCreate.as_view(), name='news_create')
]