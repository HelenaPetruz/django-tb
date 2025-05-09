# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RelTreinoExercicio(models.Model):
    id_treino = models.IntegerField(primary_key=True)  # The composite primary key (id_treino, id_exercicio) found, that is not supported. The first column is selected.
    id_exercicio = models.IntegerField()
    numero_repeticoes = models.IntegerField()
    numero_series = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rel_treino_exercicio'
        unique_together = (('id_treino', 'id_exercicio'),)
