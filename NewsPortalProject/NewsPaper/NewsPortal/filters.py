import django_filters
from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import Post, PostCategory, Author
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput
from django.forms import DateInput


class PostFilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    addtime = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата публикации',
        required=False,
    )


class PostFilter(FilterSet):
    header = CharFilter(field_name='header', lookup_expr='icontains', label='Заголовок')
    post_author = django_filters.ModelChoiceFilter(queryset=Author.objects.all())
    addtime = django_filters.DateFilter(field_name='addtime', lookup_expr='gte', label='Дата публикации',widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Post
        form_class = PostFilterForm
        fields = ['post_author', 'addtime', 'header']

