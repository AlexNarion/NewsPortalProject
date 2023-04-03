import django_filters
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, PostCategory, Author
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput


class PostFilter(FilterSet):
    date = django_filters.DateFilter(field_name="date_posted", lookup_expr='gte')
    post_author = ModelChoiceFilter(
        field_name='post__post_author',
        queryset=Author.objects.all(),
        label='Автор поста:',
    )
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
        }

