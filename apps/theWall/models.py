from django.db import models
from apps.LandR.models import User
import datetime

class PostManager(models.Manager):
    def deleteIt(self, idNum):
        a = Post.objects.get(id=idNum)
        a.delete()
    
    def itsMine(self, user, postId):
        if user == Post.objects.filter(id=postId).first().userId.id:
            return True
        return False
    
    def editing(self, idNum, text):
        edit = Post.objects.get(id=idNum)
        edit.text = text
        edit.save()

class CommentManager(models.Manager):
    def deleteIt(self, idNum):
        a = Comment.objects.get(id=idNum)
        a.delete()

    def itsMine(self, user, postId):
        if Comment.objects.filter(id=postId):
            if user == Comment.objects.get(id=postId).userId.id:
                return True
        return False
    
    def editing(self, idNum, text):
        edit = Comment.objects.get(id=idNum)
        edit.text = text
        edit.save()
    
# Create your models here.
class Post(models.Model):
    text = models.TextField()
    userId = models.ForeignKey(User, related_name = "posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    text = models.TextField()
    userId = models.ForeignKey(User, related_name = "comments")
    messageId = models.ForeignKey(Post, related_name= "comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()