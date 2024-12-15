from django.contrib import admin
from .models import Query, Synonym, ServiceWord


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "response")
    search_fields = ("text", "response")
    list_editable = ("response",)
    list_filter = ("text",)


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "synonym")
    search_fields = ("word", "synonym")
    list_filter = ("word", "synonym")


@admin.register(ServiceWord)
class ServiceWordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "word",
    )
    search_fields = ("word",)
    list_filter = ("word",)
