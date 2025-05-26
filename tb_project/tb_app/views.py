from django.shortcuts import render, redirect
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

    rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
    exercicios = list(Exercicios.objects.filter(id_exercicios__in=[rel.id_exercicio for rel in rel_treino_exercicio]))

    if 'indice' not in request.session or 'serie_atual' not in request.session or 'mostrar_descanso' not in request.session:
        request.session['indice'] = 0
        request.session['serie_atual'] = 0
        request.session['mostrar_descanso'] = False

    indice = request.session['indice']
    serie_atual = request.session['serie_atual']
    mostrar_descanso = request.session['mostrar_descanso']

    # mostrar_descanso = request.session.get('mostrar_descanso', False)
    # request.session['mostrar_descanso'] = False 
    
    if indice >= len(exercicios): #se o treino acabou
            # Zera a sessão
            request.session.pop('indice', None)
            request.session.pop('serie_atual', None)
            return redirect('home')
    
    exercicio_atual = exercicios[indice]
    rel = rel_treino_exercicio.get(id_exercicio = exercicio_atual.id_exercicios)

    if request.method == 'POST':
        
        if mostrar_descanso == False: # Primeiro clique, ativa descanso
            ultima_serie_do_ultimo_exercicio = (
                indice == len(exercicios) - 1 and
                serie_atual + 1 == rel.numero_series
            )

            if not ultima_serie_do_ultimo_exercicio:
                mostrar_descanso = True
                request.session['mostrar_descanso'] = True
                return redirect('treinoia', pk=pk)
            else:
                request.session.flush() # apaga tudo da session
                return redirect('home')

        
        else:
            # Segunda vez clicando, desativa descanso e avança série ou exercício
            mostrar_descanso = False
            request.session['mostrar_descanso'] = False

            if serie_atual+1 < rel.numero_series: #se as séries ainda não acabaram
                serie_atual +=1
            else: #se a série acabou
                if indice<len(exercicios): #vai para o próximo exercicio
                    indice+=1
                    serie_atual=0
                else: # se acabou tudo
                    request.session.flush() # apaga tudo da session
                    return redirect('home')
        
        # Atualiza sessões
        request.session['indice'] = indice
        request.session['serie_atual'] = serie_atual
        return redirect('treinoia', pk=pk)

    context={
        'rel': rel,
        'exercicio_atual': exercicio_atual,
        'serie_atual': serie_atual+1,
        'mostrar_descanso':  mostrar_descanso,
    }
    return render(request,'treinoIA.html', context)


def pagamento(request):
    return render(request, "pagamento.html")

def treino_guiado(request,pk):

    rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
    exercicios = list(Exercicios.objects.filter(id_exercicios__in=[rel.id_exercicio for rel in rel_treino_exercicio]))

    if 'indice' not in request.session or 'serie_atual' not in request.session or 'mostrar_descanso' not in request.session:
        request.session['indice'] = 0
        request.session['serie_atual'] = 0
        request.session['mostrar_descanso'] = False

    indice = request.session['indice']
    serie_atual = request.session['serie_atual']
    mostrar_descanso = request.session['mostrar_descanso']

    # mostrar_descanso = request.session.get('mostrar_descanso', False)
    # request.session['mostrar_descanso'] = False 
    
    if indice >= len(exercicios): #se o treino acabou
            # Zera a sessão
            request.session.pop('indice', None)
            request.session.pop('serie_atual', None)
            return redirect('home')
    
    exercicio_atual = exercicios[indice]
    rel = rel_treino_exercicio.get(id_exercicio = exercicio_atual.id_exercicios)

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao=="finalizar":
            if mostrar_descanso == False: # Primeiro clique, ativa descanso
                ultima_serie_do_ultimo_exercicio = (
                    indice == len(exercicios) - 1 and
                    serie_atual + 1 == rel.numero_series
                )

                if not ultima_serie_do_ultimo_exercicio:
                    mostrar_descanso = True
                    request.session['mostrar_descanso'] = True
                    return redirect('treino_guiado', pk=pk)
                else:
                    request.session.flush() # apaga tudo da session
                    return redirect('home')
           
            else:
                # Segunda vez clicando, desativa descanso e avança série ou exercício
                mostrar_descanso = False
                request.session['mostrar_descanso'] = False

                if serie_atual+1 < rel.numero_series: #se as séries ainda não acabaram
                    serie_atual +=1
                else: #se a série acabou
                    indice += 1
                    serie_atual = 0
                    if indice >= len(exercicios):  # se acabou tudo
                        request.session.flush()
                        return redirect('home')
            # Atualiza sessões
            request.session['indice'] = indice
            request.session['serie_atual'] = serie_atual
            return redirect('treino_guiado', pk=pk)
        
        elif acao=='cancelar':
            request.session.flush()
            return redirect('home')

    context={
        'rel': rel,
        'exercicio_atual': exercicio_atual,
        'serie_atual': serie_atual+1,
        'mostrar_descanso':  mostrar_descanso,
    }
    return render(request,'treinoGuiado.html', context)
