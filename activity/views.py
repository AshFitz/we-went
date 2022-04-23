from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm, PostForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'

    #maybe not needed now.
    # def get_context_data(self, **kwargs):
    #     context = super(PostList, self).get_context_data(**kwargs)
    #     context["comment_form"] = CommentForm()
    #     return context


class Comment(View):
    """
    Function to retreive the comment from Db
    """
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.order_by("created_on")
        return render(
            request,
            "add_comment.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": CommentForm()
            }
        )

    """
    Function to to add a comment to a specific post
    """
    def post(self, request, post_id, *args, **kwargs):
        queryset = Post
        post = get_object_or_404(queryset, pk=post_id)
        comments = post.comments.order_by("created_on")

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect("/")

        else:
            comment_form = CommentForm()

        return render(
            request,
            "add_comment.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": comment_form
            }
        )
"""
View to handle the like functionality of a post
"""
def like(request):
    result = 'Data'
    if request.POST.get('action') == 'post':
        result = 'Data'
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })

"""
View to add a post to the database
"""
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = request.user
            post_form.save()

            #messages.success(request, "Post Created!")
            return redirect("home")
    else:
        post_form = PostForm()
        

    context = {
        'post_form': post_form
    }
    return render(request, "add_post.html", context)