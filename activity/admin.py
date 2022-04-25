from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

class CommentItemInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['post']

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('user_profile', 'title', 'rating', 'created_on')
    search_fields = ['user_profile', 'title', 'description', 'rating']
    #prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_on', 'rating')
    summernote_fileds = ('description')
    inlines = [CommentItemInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
    
