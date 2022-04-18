from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post, Comment
from .forms import CommentForm

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class Comment(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("created_on")
        print(comments)
        return render(
            request,
            "add_comment.html",
            {
                "post": post,
                "comments": comments,
            }
        )








# def add_comment(request, slug, *args, **kwargs):
#     queryset = Post
#     post = get_object_or_404(queryset, slug=slug)
#     comments = post.comments.filter().order_by("-created_on")

#     # post = get_object_or_404(Post, pk=slug)
#     # comment = Comment.objects.filter(post=slug)


#     # comment = Post.objects.filter(slug=slug)
#     # post = get_object_or_404(comment, slug=slug)
#     print(comments)
#     print(post)
#     # post = Post.objects.filter(slug=slug)
#     # comment = get_object_or_404(post, slug=slug)

#     context = {
#         'post': post,
#         'comments': comments,
#     }

#     return render(
#         request, 'add_comment.html', context)
