from django  import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """
    Comment Form to be created when called
    """
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    """
    Form for Posts to be created.
    """
    class Meta:
        model = Post
        fields = ['title', 'location', 'rating', 'description',
                 'featured_image']

        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    "type": 'number',
                    "value": 'x out of 5',
                    "min": 1,
                    "max": 5,
                }
            )
        }
