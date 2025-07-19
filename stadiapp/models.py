from django.db import models

# Create your models here.

class Stadium(models.Model):
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name