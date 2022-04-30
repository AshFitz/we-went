from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from activity.models import Post, Comment

# Create your views here.


#Profile function

def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    profile_id = request.user.id
    print(profile_id)
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

# def post_history(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     print(post)
    
#     template = 'profiles/profile.html'
#     context = {
#         'post': post
#     }

#     return render(request, template, context)
#Post history


#likes history