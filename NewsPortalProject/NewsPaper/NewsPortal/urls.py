from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('news/create', NewsCreate.as_view, name='news_create')
]