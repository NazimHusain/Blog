from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.CustomUser import models as User


# Register your models here.


class AdminUser(admin.ModelAdmin):
    list_display = ("id","email", "username","role","profilePic")
admin.site.register(User.User, AdminUser)



class AdminTag(admin.ModelAdmin):
    list_display = ("id","name")
admin.site.register(User.Tag, AdminTag)

class AdminPost(admin.ModelAdmin):
    list_display = ("id","title","content")
admin.site.register(User.Post, AdminPost)

class AdminComment(admin.ModelAdmin):
    list_display = ("id","user","post","content","likes")
admin.site.register(User.Comment, AdminComment)

