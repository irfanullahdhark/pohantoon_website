
from django.contrib import admin
from .models import Author, Post, Comment, Category, Sub_Cat,About, Video, FacebookPost

from django.contrib import admin


class FacebookPostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FacebookPost._meta.fields]


class VideoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Video._meta.fields]


class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.fields]


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name']


class SubCatNameAdmin(admin.ModelAdmin):
    list_display = ['id','category','sub_cat_name']


class AboutAdmin(admin.ModelAdmin):
    list_display = [field.name for field in About._meta.fields]


admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Cat, SubCatNameAdmin)
admin.site.register(About, AboutAdmin)




