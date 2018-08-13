from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^addPost/$', views.createPost, name="addPost"),
    url(r'^addComment/$', views.createMessage, name="createComment"),
    url(r'^deleteComment/(?P<idNum>\d+)/$', views.deleteComment, name="deleteComment"),
    url(r'^deletePost/(?P<idNum>\d+)/$', views.deletePost, name="deletePost"),
    url(r'edit/Post/(?P<idNum>\d+)/$', views.toEditPost, name="toEditPost"),
    url(r'edit/Post/(?P<idNum>\d+)/edit/$', views.editPost, name="editPost"),
    url(r'edit/Comment/(?P<idNum>\d+)/$', views.toEditComment, name="toEditComment"),
    url(r'edit/Comment/(?P<idNum>\d+)/edit/$', views.editComment, name="editComment"),
]