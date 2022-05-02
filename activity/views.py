from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, UserProfile
from .forms import CommentForm, PostForm


class PostList(generic.ListView):
    """
    Class to query the db for posts by date created.
    """
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'

class CommentList(View):
    def get(self, request, post_id):
        """
        Function to retreive the comments from Db
        """
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


    def post(self, request, post_id, *args, **kwargs):
        """
        Function to validate if a comment form is valid,
        if so save to db and update user with a success toast.
        """
        queryset = Post
        post = get_object_or_404(queryset, pk=post_id)
        comments = post.comments.order_by("created_on")
        user = get_object_or_404(UserProfile, user=request.user)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment_form.instance.name = request.user.username
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect(reverse('post_detail', args=[post.id]))
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


@login_required
def edit_comment(request, comment_id):
    """
    View to edit a comment and update the user
    via a toast message, instanciate form on load.
    """
    user = get_object_or_404(Comment, pk=comment_id)
    if request.user == user.user:
        if request.method == "POST":
            form = CommentForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment edited.')
                return redirect(reverse('activity'))
            else:
                messages.error(request, 'Sorry please try again.')
        else:
            form = CommentForm(instance=user)
    else:
        messages.info(request, 'Oops this page is not for you')
        return redirect(reverse('activity'))
    template = 'edit_comment.html'
    context = {
        'user': user,
        'form': form,
    }
    return render(request, template, context)

@login_required
def delete_comment(request, comment_id):
    """
    View to delete a specific comment
    by the pk in the db
    """
    users_comment = get_object_or_404(Comment, pk=comment_id)
    users_comment.delete()
    messages.success(request, 'Comment deleted successfully')
    return redirect(reverse('activity'))


@login_required
def like(request):
    """
    View to handle the like functionality of a post
    """
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


@login_required
def add_post(request):
    """
    View to add a post to the database
    once form is confirmed valid, notify user
    with toast
    """
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        profile = get_object_or_404(UserProfile, user=request.user)
        MAX_SIZE = 10485759
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.user_profile = profile
            post_form.author = request.user
            if request.FILES['featured_image'].size > MAX_SIZE:
                messages.warning(request, "Your image file size is too big!")
                return redirect("add_post")
            else:
                post_form.save()
        messages.success(request, "Post Created!")
        return redirect("activity")

    else:
        post_form = PostForm()
        
    context = {
        'post_form': post_form
    }
    return render(request, "add_post.html", context)


@login_required
def edit_post(request, post_id):
    """
    View to edit a post and update the databsae
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect(reverse('edit_post', args=[post.id]))
            else:
                messages.error(request, "Failed to edit post. Please try again")

        else:
            form = PostForm(instance=post)
            messages.info(request, f'You are editing {post.title}')
    else: 
        return redirect(reverse('activity'))
        form = None
        messages.success(request, "Your post has been updated!")

    template = 'edit_post.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """
    View to delete a post and update the database
    """
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, 'Your post has been deleted')
    return redirect(reverse('activity'))


def search_posts(request):
    """
    View to search post in the database
    """
    posts = Post.objects.all()
    if request.method == "POST":
        search = request.POST.get('search-input')
        queries = Q(title__icontains=search) | Q(
            description__icontains=search) | Q(
            location__icontains=search)
        posts = posts.filter(queries)
        if not posts:
            messages.info(request, "Sorry we couldn't find a post that matched your search, here is some posts you may like")
            return redirect(reverse('activity'))

    context = {
        'post_search': posts,
        'search': search,
    }
    return render(request, 'searched_posts.html', context)


def post_detail(request, post_id):
    """
    View to click into individual post
    """
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.order_by("created_on")
    context= {
        'post' : post,
        'comments' : comments
    }
    return render(request, 'post_detail.html', context)
