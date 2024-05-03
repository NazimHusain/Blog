from django.db import models
from apps.CustomUser.managers import CustomUserManager
from apps.Helpers import models as coreModels
from django.contrib.auth.models import AbstractUser

from uuid import uuid4
# Create your models here.

class User(AbstractUser):
    """Model for saving basic user info."""

    email = models.EmailField("email address", unique=True, null=True, blank=True)
    username = models.EmailField("username", unique=True)  
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    role = models.ForeignKey(
        coreModels.DropdownValues, null=True, blank=True, on_delete=models.PROTECT
    )
    profilePic = models.ForeignKey(
        coreModels.FileUpload,
        null=True,
        blank=True,
        related_name="user_profile_pic",
        on_delete=models.PROTECT,
    )
   

    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self: "User") -> str:
        return str(self.username)
    

class Tag(coreModels.AbstractDateTimeModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(coreModels.AbstractDateTimeModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='post')

    def __str__(self):
        return self.title

class Comment(coreModels.AbstractDateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'


