from django.db import models

# Create your models here.

class Stadium(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sport = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name