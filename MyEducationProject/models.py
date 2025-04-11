# Create your models here.
from django.db import models


class MusicTerm(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    m_term = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'music_terms'
