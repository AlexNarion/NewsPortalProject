from django import forms
from.models import Post, PostCategory, Author
from .filters import PostFilter


class PostFilterForm(PostFilter.form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'tape': 'date'}),
        required=False,
        label='Дата позже:'
    )
    class Meta:
        model = PostFilter.Meta.model
        fields = PostFilter.Meta.model

class PostForm(forms.ModelForm):
    post_author = forms.CharField(max_length=100)
    category = forms.ModelChoiceField(queryset=PostCategory.category.objects.all(required=False)
    header = forms.CharField(max_length=50)
    text  = forms.CharField

    class Meta:
        model = Post
        fields = ['post_author','category','header','text']



