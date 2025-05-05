from django.shortcuts import render
import random
from .models import Exercicios, Treino, NivelDificuldade, MusculosEnvolvidos, RelExerciciosMusculos, Plano, RelTreinoExercicio

def home(request):
    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    numero_aleatorio = random.randint(1, exercicios_count)
    exercicio = Exercicios.objects.get(id_exercicios= numero_aleatorio)
    planos = Plano.objects.all()

    context ={
        'exercicio': exercicio,
        'planos': planos,
    }
    return render(request, 'home.html', context)

def exercicios(request):
    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    context = {
        'exercicios': exercicios,
        'exercicios_count': exercicios_count,
    }
    return render(request, 'exercicios.html', context)

def treinos(request):
    treinos = Treino.objects.all()
    context = {
        'treinos': treinos,
    }
    return render(request, 'treinos.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

def montagem_treinos(request):
    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    context = {
        'exercicios': exercicios,
        'exercicios_count': exercicios_count,
    }
    return render(request, 'montagemTreinos.html', context) 

def meus_treinos(request):
    return render(request, 'meusTreinos.html')

def exercicio(request, pk):
    exercicio = Exercicios.objects.get(id_exercicios=pk)
    rel_exercicios_musculos = RelExerciciosMusculos.objects.filter(id_exercicio=pk)
    musculos = MusculosEnvolvidos.objects.filter(id_musculos_envolvidos__in=[rel.id_musculo for rel in rel_exercicios_musculos])
    context={
        'exercicio': exercicio,
        'rel_exercicios_musculos': rel_exercicios_musculos,
        'musculos': musculos,
    }
    return render(request, 'pgExercicio.html', context)

def treino(request, pk):
    treino = Treino.objects.get(id=pk)
    rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
    exercicios = Exercicios.objects.filter(id_exercicio__in=[rel.id_exercicio for rel in rel_treino_exercicio])
    context={
        'treino': treino,
        'exercicios': exercicios,
    }
    return render(request, 'pgTreino.html', context)

