from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Todo(models.Model):
    objects = None
    titre = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    datecreation = models.DateTimeField(auto_now_add=True)
    dateacheve = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre
