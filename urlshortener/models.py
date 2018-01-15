from django.db import models

# Create your models here.

class urls(models.Model):
    original = models.URLField()
    alias = models.CharField(max_length = 15, unique = True)
    count = models.PositiveIntegerField(default=0)
    link = models.CharField(max_length = 264, unique = True)
    custom = models.BooleanField(default = False)

    def __str__(self):
        return self.link
