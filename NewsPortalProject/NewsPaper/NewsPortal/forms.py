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
    class Meta:
        model = Post
        fields = ['post_author','category','header','text','category']



