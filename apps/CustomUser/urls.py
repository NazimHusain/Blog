from django.urls import path
from apps.CustomUser import views

urlpatterns = [
    path("register/", (views.SignUp.as_view())),
    path("login/", views.UserLogin.as_view()),
    path("logout/", views.UserLogout.as_view()),
    path("tag/", views.TagAPIView.as_view()),
    path("post/", views.PostSearchAPIView.as_view()),
    path("post/<int:postId>/", views.PostDetails.as_view()),
    path("comment/", views.CommentAPIView.as_view()),
]



