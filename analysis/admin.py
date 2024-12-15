from django.contrib import admin
from .models import Query, ServiceWord, SynonymGroup, Word


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "response")
    search_fields = ("text", "response")
    list_editable = ("response",)
    list_filter = ("text",)


@admin.register(SynonymGroup)
class SynonymGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "group")
    search_fields = ("text", "group__name")
    list_filter = ("group",)
    ordering = ("group", "text")
    autocomplete_fields = ["group"]


@admin.register(ServiceWord)
class ServiceWordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "word",
    )
    search_fields = ("word",)
    list_filter = ("word",)
