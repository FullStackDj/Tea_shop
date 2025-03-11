from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'text_on_page')
    search_fields = ('title', 'content')
