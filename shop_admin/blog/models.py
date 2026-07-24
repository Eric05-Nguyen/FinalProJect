from datetime import timezone
from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from admin_shop.settings import AUTH_USER_MODEL 

class Blog(models.Model):
    title= models.CharField(max_length=300)
    description = models.TextField()
    content = CKEditor5Field('Content',config_name='default')
    image=models.ImageField(upload_to='blog_images/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table="blog"


class Rates(models.Model):
    rates=models.IntegerField()
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment=models.TextField()
    author_name=models.TextField()
    author_image=models.ImageField(upload_to='comment_images/',null=False,blank=False)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    level=models.IntegerField(default=0)
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    