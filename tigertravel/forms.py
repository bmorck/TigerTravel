from django import forms
from .models import Group

class CommentForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('text',)