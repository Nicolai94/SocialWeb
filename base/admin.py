from django.contrib import admin
from django.utils.safestring import mark_safe

from base.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_photo']
    search_fields = ['username']

    def get_photo(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50">')
        return '-'

    get_photo.short_description = 'Mark'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['host', 'topic', 'name', 'description', 'created']
    list_filter = ['created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['topic']
    save_as = True
    save_on_top = True


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created']
    list_filter = ['created']
    search_fields = ['user']
    save_as = True
    save_on_top = True


