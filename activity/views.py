from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Post, Comment, UserProfile
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
                "comment_form": CommentForm(),
                
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
View to edit a comment on a post
"""
def edit_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(Comment, user=request.user, post=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=user)
        if comment_form.is_valid():
            comment_form.save()
            # messages.success(request, f'You have updated your comment on {post.title}.')
            return redirect(reverse('edit_comment', args=[post_id]))
        # else:
            # messages.error(request, f'Sorry we are unable to update your comment on {post.title}, please try again.')
    else:
        comment_form = CommentForm(instance=user)

    template = 'edit_post.html'
    context = {
        'post': post,
        'user': user,
        'comment_form': comment_form,
    }
    return render(request, template, context)


def delete_comment(request, post_id):
    comment = get_object_or_404(Comment, user=request.user, post=post_id)
    comment.delete()
    #message.success(request, 'Your comment has been deleted.')
    return redirect(reverse('home'))

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
        profile = get_object_or_404(UserProfile, user=request.user)

        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.user_profile = profile
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


"""
View to edit a post and update the databsae
"""
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('edit_post', args=[post.id]))
        else:
            print("do this")
            #messages.error(request, "Failed to edit post. Please try again")

    else:
        form = PostForm(instance=post)
        #messages.info(request, f'You are editing {post.tilte}')

    post_title = 'Edit a post'
    template = 'edit_post.html'
    context = {
        'form':form,
        'post':post,
    }

    return render(request, template, context)


"""
View to delete a post and update the database
"""
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    #messages.sucess(request, 'You have deleted your post")

    return redirect(reverse('home'))


"""
View to search post in the database
"""

def search_posts(request):
    posts = Post.objects.all()


    if request.method == "POST":
        search = request.POST.get('search-input')
        queries = Q(title__icontains=search) | Q(
            description__icontains=search) | Q(
            location__icontains=search)
        posts = posts.filter(queries)

        if not posts:
            # messages.info(request, "Sorry we couldn't find a post that matched your search.")
            return redirect(reverse('home'))

    context = {
        'post_search': posts,
        'search': search,
    }

    return render(request, 'searched_posts.html', context)