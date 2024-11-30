from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    gender = models.BooleanField(default=True)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/avatars/avatar_default.png",
        null=True,
        blank=True,
    )
    is_normal_user = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, related_name="user_w_profile", on_delete=models.CASCADE, primary_key=True
    )


class Knowledge(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="images/knowledge/",
        null=True,
        blank=True,
    )
    short_description = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name="user_knowledges", on_delete=models.CASCADE
    )
    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    imgUrl = models.ImageField(upload_to="category_images/", null=True, blank=True)
    navigationPath = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Expert(models.Model):
    jobTitle = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="experts/", null=True, blank=True)
    bio = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating = models.FloatField()
    reviews = models.IntegerField()
    user = models.OneToOneField(
        User, related_name="user_w_expert", on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.jobTitle


class EmergencyHelp(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    imgUrl = models.ImageField(upload_to="emergency_elp_images/", null=True, blank=True)

    def __str__(self):
        return self.name


class Stories(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="images/stories/",
        null=True,
        blank=True,
    )
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User,
        related_name="user_w_stories",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.title
    
class PrivateChat(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chats_as_user1')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chats_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Đảm bảo không tạo trùng chat giữa 2 user

class Message(models.Model):
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

