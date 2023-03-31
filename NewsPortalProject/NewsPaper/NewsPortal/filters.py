import django_filters
from django_filters import FilterSet, ModelChoiceFilter,Filter
from .models import Post, PostCategory, Author
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput


class DateFilter(Filter):
    field_class = django_filters.filters.DateRangeField
    widget = RangeWidget(attrs={'type':'date'})


class PostFilter(FilterSet):
    post_author = ModelChoiceFilter(
        field_name='post__post_author',
        queryset=Author.objects.all(),
        label='Post Author',
    )
    date_range = DateFilter(field_name='created_at', label='Created At')
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
        }

