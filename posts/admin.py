from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("caption", "author", "created_at")
    search_fields = ("caption",)
