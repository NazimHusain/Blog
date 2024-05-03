from django.urls import path
from apps.CustomUser import views

urlpatterns = [
    path("register/", (views.SignUp.as_view())),
    path("login/", views.UserLogin.as_view()),
    path("logout/", views.UserLogout.as_view()),
    path("tag/", views.TagAPIView.as_view()),
    path("post/", views.PostSearchAPIView.as_view()),
    path("post/<int:postId>/", views.PostDetails.as_view()),

    # path("me/", views.Me.as_view()),
    # path("updateprofile/", views.UpdateProfile.as_view()),
]



# pagination
# Adding the tagging functionality and searching based on tags
# Adding full text search from the blog data
# Stemming and ranking result
# Searching with trigram similarity

# Create a comment system on any blog and add like option to like the comment
# Share the blog through email