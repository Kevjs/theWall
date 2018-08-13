from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import Post, Comment, User
import datetime
from django.contrib import messages

# Create your views here.
def home(request):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    context = {
        "posts": Post.objects.all().order_by("-id")
    }
    return render(request, "theWall/index.html", context)

def createPost(request):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    Post.objects.create(text = request.POST["postText"], userId = User.objects.get(id = request.session["userid"]))
    return redirect(reverse("theWall:home"))

def createMessage(request):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    user = User.objects.filter(id = request.session["userid"]).first()
    post = Post.objects.filter(id = request.POST["postId"]).first()
    Comment.objects.create(userId = user, text = request.POST["comment"], messageId = post)
    return redirect(reverse("theWall:home"))

def deleteComment(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    if Comment.objects.itsMine(request.session["userid"], idNum):
        Comment.objects.deleteIt(idNum)
    return redirect(reverse("theWall:home"))

def deletePost(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    if Post.objects.itsMine(request.session["userid"], idNum):
        Post.objects.deleteIt(idNum)
    return redirect(reverse("theWall:home"))

def toEditPost(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    naive = Post.objects.get(id=idNum).updated_at.replace(tzinfo=None)
    if (datetime.datetime.utcnow() - naive) > datetime.timedelta(minutes=30):
        messages.add_message(request, messages.INFO, "It's been too long to edit", extra_tags=int(idNum))
        return redirect(reverse("theWall:home"))
    if Post.objects.itsMine(request.session["userid"], idNum):
        return render(request, "theWall/editPost.html", {"post" : Post.objects.get(id=idNum)})
    return redirect(reverse("theWall:home"))

def editPost(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    if Post.objects.itsMine(request.session["userid"], idNum):
        naive = Post.objects.get(id=idNum).updated_at.replace(tzinfo=None)
        if (datetime.datetime.utcnow() - naive) < datetime.timedelta(minutes=30):
            Post.objects.editing(idNum, request.POST["postText"])
        else:
            messages.add_message(request, messages.INFO, "It's been too long to edit", extra_tags=int(idNum))
    return redirect(reverse("theWall:home"))

def toEditComment(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    naive = Comment.objects.get(id=idNum).updated_at.replace(tzinfo=None)
    if (datetime.datetime.utcnow() - naive) > datetime.timedelta(minutes=3):
        messages.add_message(request, messages.INFO, "It's been too long to edit", extra_tags=int(idNum))
        return redirect(reverse("theWall:home"))
    if Comment.objects.itsMine(request.session["userid"], idNum):
        return render(request, "theWall/editComment.html", {"comment" : Comment.objects.get(id=idNum), "post" : Comment.objects.get(id=idNum).messageId})
    return redirect(reverse("theWall:home"))

def editComment(request, idNum):
    if "userid" not in request.session:
        return redirect(reverse("login:home"))
    if Comment.objects.itsMine(request.session["userid"], idNum):
        naive = Comment.objects.get(id=idNum).updated_at.replace(tzinfo=None)
        if (datetime.datetime.utcnow() - naive) < datetime.timedelta(minutes=30):
            Comment.objects.editing(idNum, request.POST["commentText"])
        else:
            messages.add_message(request, messages.INFO, "It's been too long to edit", extra_tags=int(idNum))
    return redirect(reverse("theWall:home"))