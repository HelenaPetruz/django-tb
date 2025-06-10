# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    adm = models.IntegerField(blank=True, null=True)
    ativado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perfil'


class Pessoa(models.Model):
    idpessoa = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=45, blank=True, null=True)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=130, blank=True, null=True)
    id_plano = models.IntegerField(blank=True, null=True)
    id_perfil = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoa'

    def __str__(self):
        return self.nome_usuario
    
class RelUsuarioTreino(models.Model):
    id_treino = models.IntegerField(primary_key=True)  # The composite primary key (id_treino, id_usuario) found, that is not supported. The first column is selected.
    id_usuario = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rel_usuario_treino'
        unique_together = (('id_treino', 'id_usuario'),)


class Plano(models.Model):
    id_plano = models.AutoField(primary_key=True)
    nome_plano = models.CharField(max_length=45)
    valor = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'plano'

    def __str__(self):
        return self.nome_plano


class CondPagamento(models.Model):
    id_cond_pagamento = models.AutoField(primary_key=True)
    numero_do_cartao = models.CharField(max_length=45)
    nome = models.CharField(max_length=45)
    id_plano = models.IntegerField()
    data_validade = models.CharField(max_length=45)
    cvv = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'cond_pagamento'

    def __str__(self):
        return self.nome

class NivelDificuldade(models.Model):
    idnivel_dificuldade = models.IntegerField(primary_key=True)
    nome_nivel_dificuldade = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nivel_dificuldade'

class Exercicios(models.Model):
    id_exercicios = models.IntegerField(primary_key=True)  # The composite primary key (id_exercicios, id_nivel_dificuldade_id) found, that is not supported. The first column is selected.
    nome_exercicio = models.CharField(max_length=45)
    descricao = models.CharField(max_length=1000)
    id_nivel_dificuldade = models.ForeignKey('NivelDificuldade', models.DO_NOTHING)
    imagem = models.ImageField(null=True, default="tb.png", upload_to='exercicios/')
    link_ia = models.CharField(db_column='link_IA', max_length=150, blank=True, null=True)  # Field name made lowercase.
    video = models.FileField(max_length=45, blank=True, null=True, upload_to='videos/')

    class Meta:
        managed = False
        db_table = 'exercicios'
        unique_together = (('id_exercicios', 'id_nivel_dificuldade'), ('id_exercicios', 'id_nivel_dificuldade'),)
    def __str__(self):
        return self.nome_exercicio

class Treino(models.Model):
    id_treino = models.AutoField(primary_key=True)
    nome_treino = models.CharField(max_length=45)
   

    class Meta:
        managed = False
        db_table = 'treino'

    def __str__(self):
        return self.nome_treino


class RelExerciciosMusculos(models.Model):
    id_musculo = models.IntegerField(primary_key=True)  # The composite primary key (id_musculo, id_exercicio) found, that is not supported. The first column is selected.
    id_exercicio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rel_exercicios_musculos'
        unique_together = (('id_musculo', 'id_exercicio'),)


class RelPlanoTreino(models.Model):
    id_treino = models.IntegerField(primary_key=True)  # The composite primary key (id_treino, id_plano) found, that is not supported. The first column is selected.
    id_plano = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'rel_plano_treino'
        unique_together = (('id_treino', 'id_plano'),)


class RelTreinoExercicio(models.Model):
    id_treino = models.IntegerField(primary_key=True)  # The composite primary key (id_treino, id_exercicio) found, that is not supported. The first column is selected.
    id_exercicio = models.IntegerField()
    numero_repeticoes = models.IntegerField()
    numero_series = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rel_treino_exercicio'
        unique_together = (('id_treino', 'id_exercicio'),)


class MusculosEnvolvidos(models.Model):
    id_musculos_envolvidos = models.AutoField(primary_key=True)
    nome_musculo = models.CharField(max_length=45, blank=True, null=True)
    imagem = models.ImageField(null=True, default="tb.png", upload_to='musculos/')

    class Meta:
        managed = False
        db_table = 'musculos_envolvidos'

class ErrosPossiveis(models.Model):
    id_erro = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=1000, blank=True, null=True)
    id_exercicio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'erros_possiveis'