from django import forms
from django.forms import Textarea

from.models import Post, PostCategory, Author, Comment
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
        fields = ['category','header','text','category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['comment_text'].widget = Textarea(attrs={'rows':5})