# Generated by Django 5.1.6 on 2025-04-28 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb_app', '0004_alter_exercicios_id_nivel_dificuldade'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelExerciciosMusculos',
            fields=[
                ('id_musculo', models.IntegerField(primary_key=True, serialize=False)),
                ('id_exercicio', models.IntegerField()),
            ],
            options={
                'db_table': 'rel_exercicios_musculos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RelPlanoTreino',
            fields=[
                ('id_treino', models.IntegerField(primary_key=True, serialize=False)),
                ('id_plano', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'rel_plano_treino',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RelTreinoExercicio',
            fields=[
                ('id_treino', models.IntegerField(primary_key=True, serialize=False)),
                ('id_exercicio', models.CharField(max_length=45)),
                ('numero_repeticoes', models.IntegerField()),
                ('numero_series', models.IntegerField()),
            ],
            options={
                'db_table': 'rel_treino_exercicio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MusculosEnvolvidos',
            fields=[
                ('id_musculos_envolvidos', models.AutoField(primary_key=True, serialize=False)),
                ('nome_musculo', models.CharField(blank=True, max_length=45, null=True)),
                ('imagem', models.ImageField(default='tb.png', null=True, upload_to='musculos/')),
            ],
            options={
                'db_table': 'musculos_envolvidos',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='exercicios',
            name='musculos_envolvidos',
        ),
        migrations.AddField(
            model_name='exercicios',
            name='link_ia',
            field=models.CharField(blank=True, db_column='link_IA', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='exercicios',
            name='id_nivel_dificuldade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tb_app.niveldificuldade'),
        ),
    ]
