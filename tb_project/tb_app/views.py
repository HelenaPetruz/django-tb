from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
import random
from django.contrib import messages
from .models import Exercicios, Treino, NivelDificuldade, MusculosEnvolvidos, RelExerciciosMusculos, Plano, RelTreinoExercicio, ErrosPossiveis, CondPagamento, Pessoa

def home(request):

    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    numero_aleatorio = random.randint(1, exercicios_count)
    exercicio = Exercicios.objects.get(id_exercicios= numero_aleatorio)
    planos = Plano.objects.exclude(id_plano=4)

    context ={
        'exercicio': exercicio,
        'planos': planos,
    }

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        context ={
            'exercicio': exercicio,
            'planos': planos,
            'pessoa': pessoa,
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
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')

        if senha1!=senha2:
            messages.error(request, 'Os campos de senha devem ser preenchidos com a mesma senha!')
            context={
                'nome': nome,
                'email': email,
            }
            return redirect('cadastro', context)
        if Pessoa.objects.filter(email=email).exists():
            messages.error(request, 'Esse email já existe!')
            return redirect('cadastro')
            
    
        pessoa = Pessoa(
            nome_usuario = nome,
            email=email,
            senha=make_password(senha1),
            id_plano = 4,
            id_perfil = 1
        )
        pessoa.save()
        return redirect('home')
    
    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        try:
            pessoa = Pessoa.objects.get(email=email)
            if check_password(senha, pessoa.senha):
                request.session['pessoa_id'] = pessoa.idpessoa
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta!')

        except Pessoa.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
            return redirect('login')
    
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')

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
    
    erros_possiveis = ErrosPossiveis.objects.filter(id_exercicio=exercicio_atual.id_exercicios)

    context={
        'rel': rel,
        'exercicio_atual': exercicio_atual,
        'serie_atual': serie_atual+1,
        'mostrar_descanso':  mostrar_descanso,
        'erros': erros_possiveis
    }
    return render(request,'treinoIA.html', context)

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
        # acao = request.POST.get('acao')
        # if acao=="finalizar":
        
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
        return redirect('treino_guiado', pk=pk)
        
        # if acao=="cancelar":
        #     #request.session.flush()
        #     request.session['indice'] = 0
        #     request.session['serie_atual'] = 0
        #     request.session['mostrar_descanso'] = False
        #     return redirect('home')
        

    context={
        'rel': rel,
        'exercicio_atual': exercicio_atual,
        'serie_atual': serie_atual+1,
        'mostrar_descanso':  mostrar_descanso,
    }
    return render(request,'treinoGuiado.html', context)

def pagamento(request):
    # if request.method == 'POST':
    #     CondPagamento.objects.create(
    #         numero_do_cartao = request.POST.get('numero_cartao'),
    #     )

    return render(request, "pagamento.html")