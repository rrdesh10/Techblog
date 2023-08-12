from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta():
        fields = ('author', 'title', 'text')
        model = Post

    widgets = {
        'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        'text': forms.TextInput(attrs={'class': 'editable medium-editor-textarea postcontent'})
    }


class CommentForm(forms.ModelForm):

    class Meta():
        fields = ('author', 'text')
        model = Comment

    widgets = {
        'author': forms.TextInput(attrs={'class': 'textinputclass'}),
        'text': forms.TextInput(attrs={'class': 'editable medium-editor-textarea'})
    }
