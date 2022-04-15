from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post, Comment

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'


# class PostDetails(View):

#     def get(self, request, *args, **kwargs):
#         queryset = Post.objects.all()
#         # post = queryset.
#         # comments = post.comments.order_by('-created_on')

#         return render(
#             request,
#             "index.html",
#             {
#                 # "post" : post,
#                 # "comments" : comments,
#             },
#         )