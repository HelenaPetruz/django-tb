from django.shortcuts import render
from .models import Exercicios, Treino, NivelDificuldade

def home(request):
    return render(request, 'home.html')

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
    context={
        'exercicio': exercicio,
    }
    return render(request, 'pgExercicio.html', context)

def treino(request, pk):
    treino = Treino.objects.get(id=pk)
    context={
        'treino': treino,
    }
    return render(request, 'pgTreino.html', context)