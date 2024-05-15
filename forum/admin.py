from django.contrib import admin
from forum.models import *
from django.contrib.admin import ModelAdmin

# Register your models here.

class MessageView(ModelAdmin):
    list_display = ['author', 'topic', 'text', 'image']
    search_fields = ['text']
    empty_value_display = 'Не задано'
    list_filter = ['author', 'topic']


admin.site.register(Profile)
admin.site.register(Message, MessageView)
admin.site.register(Topic)
admin.site.register(Chapter)