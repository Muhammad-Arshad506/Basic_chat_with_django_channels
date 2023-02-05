from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "text", "message_time", "is_delivered"]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "room", "get_member", "admin"]

    def get_member(self, obj):
        return list(obj.member.all()) if obj.member.all() else 'NA'


@admin.register(GroupMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["group", "text", "sender", "message_time"]
