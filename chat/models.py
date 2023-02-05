from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


# Create your models here.


class Message(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    text = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ["-message_time"]


class Group(models.Model):
    name = models.CharField(max_length=50)
    room = models.UUIDField(default=uuid4())
    member = models.ManyToManyField(to=get_user_model(), related_name="group_member")
    admin = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="group_admin")

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    text = models.TextField()
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name="group_message")
    sender = models.CharField(max_length=50)
    message_time = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.text
