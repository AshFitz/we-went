from . import views
from django.urls import path

urlpatterns = [
    path('like/', views.like, name='like'),
    path("add/", views.add_post, name="add_post"),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    #path('post/<int:pk>', views.add_post, name="post_detail"),
    path("activity/", views.PostList.as_view(), name="activity"),
    path('comment/<int:post_id>/', views.CommentList.as_view(), name='comment'),
    path('searched_posts/', views.search_posts, name='searched_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail')
]