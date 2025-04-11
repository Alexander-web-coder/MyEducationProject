# Create your models here.
'''Модель для базы'''
from django.db import models


class MusicTerm(models.Model):
    '''Класс для нашей базы с терминами'''
    id = models.AutoField(primary_key=True, null=False)
    m_term = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)

    class Meta:
        '''Служебный класс для операций с таблицей music_terms'''
        managed = True
        db_table = 'music_terms'
