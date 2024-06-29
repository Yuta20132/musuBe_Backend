from django.db import models
from users.models import User

#掲示板のエンティティ
class Thread(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=255)

#投稿のエンティティ
class Post(models.Model):
    threads = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#コメントのエンティティ
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)