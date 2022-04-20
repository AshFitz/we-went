from . import views
from django.urls import path

urlpatterns = [
    path('like/', views.like, name='like'),
    path("", views.PostList.as_view(), name="home",),
    path('<slug:slug>/', views.Comment.as_view(), name='comment'),  
    #path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
]