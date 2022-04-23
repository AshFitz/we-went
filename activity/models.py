from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Post(models.Model):
    title = models.CharField(max_length=220, unique=True)
    location = models.CharField(max_length=220)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2)
    #slug = models.SlugField(max_length=220, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_post")
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    featured_image = CloudinaryField('image', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='activity_likes', blank=True)
    like_count = models.BigIntegerField(default='0')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def liked_by_user(self):
        return self.likes.values_list('id', flat=True)


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

