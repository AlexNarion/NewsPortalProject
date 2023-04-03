from django import forms
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