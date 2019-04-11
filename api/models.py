from django.db import models
from django.db.models import F


class Url(models.Model):

    id = models.AutoField(primary_key=True)
    original_url = models.URLField(db_column="OriginalUrl")
    alias = models.CharField(max_length=15, unique=True, db_column="Alias")
    hits = models.PositiveIntegerField(default=0, db_column="Hits")

    class Meta:
        db_table = 'Url'

    def hit(self):
        self.hits = F('hits') + 1
        self.save()
