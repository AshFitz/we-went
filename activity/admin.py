from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


class CommentItemInline(admin.TabularInline):
    """
    Admin panel comment item inline
    """
    model = Comment
    raw_id_fields = ['post']

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin panel to show the post information
    """
    list_display = ('user_profile', 'title', 'rating', 'created_on')
    search_fields = ['user_profile', 'title', 'description', 'rating']
    list_filter = ('created_on', 'rating')
    summernote_fileds = ('description')
    inlines = [CommentItemInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin view of comments
    """
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')
    
