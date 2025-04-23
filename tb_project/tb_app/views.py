from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def exercicios(request):
    return render(request, 'exercicios.html')

def treinos(request):
    return render(request, 'treinos.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

def montagem_treinos(request):
    return montagem_treinos(request, 'montagemTreinos.html') 

def meus_treinos(request):
    return meus_treinos(request, 'meusTreinos.html')