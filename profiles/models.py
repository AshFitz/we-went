from django.db import models, Post
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A user profile model to link posts and likes
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
   


