from .models import Comment, Post
from django  import forms



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'location', 'rating', 'description', 
                 'featured_image']

        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    "type": 'number',
                    "value": 1,
                    "min": 1,
                    "max": 5,
                }
            )
        }