from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from activity.models import Post

# Create your views here.


#Profile function

def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    posts = profile.user_posts.all()
    # posts = profile.post_set.all()
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
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