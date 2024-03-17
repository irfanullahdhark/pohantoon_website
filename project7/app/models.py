from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from embed_video.fields import EmbedVideoField


# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=200)

    def __str__(self):
        return self.cat_name


class Sub_Cat(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_category')
    sub_cat_name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='sub_categories/')

    def __str__(self):
        return self.sub_cat_name


def subcat_image_dimension_validator(image):
    width, height = image.width, image.height
    if width != 300 and height != 374:
        raise ValidationError('Sub Category image dimensions must be (300x374) ')


class Author(AbstractUser):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='authors/', validators=[subcat_image_dimension_validator])
    info = models.TextField(null=True,blank=True)
    no_post = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.name



def post_image_dimension_validator(image):
    width, height = image.width, image.height
    if width != 840 and height != 870:
        raise ValidationError('Post image dimensions must be (840x870) ')


class Post(models.Model):
    post_author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='post_authors')
    orginal_source_name = models.CharField(max_length=150,null=True,blank=True)
    title = models.CharField(max_length=600)
    image = models.ImageField(upload_to='posts/',validators=[post_image_dimension_validator])
    post_cat = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='post_cat')
    sub_cat = models.ForeignKey(Sub_Cat,on_delete=models.CASCADE,related_name='post_sub')
    date = models.DateTimeField()
    view = models.IntegerField(null=True,blank=True,default=0)
    description = HTMLField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def about_image_dimension_validator(image):
    width, height = image.width, image.height
    if width != 1918 and height != 670:
        raise ValidationError('About image dimensions must be (1918x670) ')


class About(models.Model):
    image = models.ImageField(upload_to='about/',validators=[about_image_dimension_validator])
    bio = models.TextField()
    description = HTMLField()


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    replay = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE,related_name='replay_comment')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=600)
    link = EmbedVideoField()
    main_cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='main_videos')
    sub_cat = models.ForeignKey(Sub_Cat, on_delete=models.CASCADE, related_name='sub_videos')
    views = models.IntegerField(null=True,blank=True, default=0)
    date = models.DateTimeField()


class FacebookPost(models.Model):
    post_html = models.TextField()
    date = models.DateTimeField()






