from django import forms
from .models import Post, Comment #oluşturduğumuz modelleri import ettik


class PostForm(forms.ModelForm):

    class Meta:
        model = Post #PostForm class ını Post modeline bağladık
        fields = ('author','title', 'text',) #ve düzenlemek istediğimz alanları veriyoruz

        widgets = {    #alanlara ekstra özellik kazandırmak için CSS widgets kullandık
            'title': forms.TextInput(attrs={'class': 'textinputclass'}), 
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment #CommentForm class ını Comment modeline bağladık
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
