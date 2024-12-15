from django.db import models


class Query(models.Model):
    text = models.TextField(unique=True)
    response = models.TextField()

    def __str__(self):
        return f"Query{self.text}"


class SynonymGroup(models.Model):
    name = models.CharField(
        max_length=255, unique=True, help_text="Уникальное имя группы синонимов"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SynonymGroup {self.name}"


class Word(models.Model):
    text = models.CharField(max_length=255, unique=True)
    group = models.ForeignKey(
        SynonymGroup, on_delete=models.SET_NULL, related_name="words", null=True
    )

    def __str__(self):
        return self.text


class ServiceWord(models.Model):
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"ServiceWord {self.word}"
