from django.contrib import admin
from forum.models import *
from django.contrib.admin import ModelAdmin

# Register your models here.

class MessageView(ModelAdmin):
    list_display = ['author', 'question', 'text', 'image']
    search_fields = ['text']
    empty_value_display = 'Не задано'
    list_filter = ['author', 'question']


admin.site.register(Profile)
admin.site.register(Message, MessageView)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(Question)