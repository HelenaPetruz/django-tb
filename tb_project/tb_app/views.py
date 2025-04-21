from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def exercicios(request):
    return render(request, 'exercicios.html')

def treinos(request):
    return render(request, 'treinos.html')