from . import views
from django.urls import path

urlpatterns = [
    path('like/', views.like, name='like'),
    path("add/", views.add_post, name="add_post"),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
    #path('post/<int:pk>', views.add_post, name="post_detail"),
    path("", views.PostList.as_view(), name="home"),
    path('comment/<int:post_id>/', views.Comment.as_view(), name='comment'),
    #path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
]