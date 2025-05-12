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
    return render(request, 'treinos.html', context)

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
    treino = Treino.objects.get(id_treino=pk)
    rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
    exercicios = Exercicios.objects.filter(id_exercicios__in=[rel.id_exercicio for rel in rel_treino_exercicio])
    context={
        'treino': treino,
        'exercicios': exercicios,
        'rels': rel_treino_exercicio,
    }
    print([rel.id_exercicio for rel in rel_treino_exercicio])
    print([exercicio.id_exercicios for exercicio in exercicios])
    return render(request, 'pgTreino.html', context)

def treinoia(request,pk):
    treino = Treino.objects.get(id_treino=pk)
    rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
    exercicios = Exercicios.objects.filter(id_exercicios__in=[rel.id_exercicio for rel in rel_treino_exercicio])
    context={
        'treino': treino,
        'exercicios': exercicios,
        'rels': rel_treino_exercicio,
    }
    return render(request,'treinoIA.html', context)

def pagamento(request):
    return render(request, "pagamento.html")
