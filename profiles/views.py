from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from activity.models import Post

# Create your views here.


#Profile function

def profile(request):
    #profile = UserProfile.objects.create(user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
   
   
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        # 'posts': posts
    }

    return render(request, template, context)


#Post history


#likes history