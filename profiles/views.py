from django.shortcuts import render, get_object_or_404
from activity.models import Post, Comment
from .models import UserProfile


def profile(request):
    """
    View to get users profile
    display posts and likes
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    posts = profile.user_posts.all()
    likes = Post.objects.filter(likes=request.user.id)
    comments = Comment.objects.order_by('created_on')
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'comments': comments,
        'likes': likes,
        'posts': posts
    }

    return render(request, template, context)