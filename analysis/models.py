from django.db import models


class Query(models.Model):
    text = models.TextField(unique=True)
    response = models.TextField()

    def __str__(self):
        return f"Queryт{self.text}"


class Synonym(models.Model):
    word = models.CharField(max_length=255)
    synonym = models.CharField(max_length=255)

    def __str__(self):
        return f"Synonym {self.word} -> {self.synonym}"


class ServiceWord(models.Model):
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"ServiceWord {self.word}"
