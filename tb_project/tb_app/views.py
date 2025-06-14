from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
import random
from django.contrib import messages
from .models import Exercicios, Treino, NivelDificuldade, MusculosEnvolvidos, RelExerciciosMusculos, Plano, RelTreinoExercicio, ErrosPossiveis, CondPagamento, Pessoa, RelUsuarioTreino

def home(request):

    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    numero_aleatorio = random.randint(1, exercicios_count)
    exercicio = Exercicios.objects.get(id_exercicios= numero_aleatorio)
    planos = Plano.objects.exclude(id_plano=4)
    

    #popups
    cadastro_sucesso = request.session.pop('cadastro_sucesso', False)
    login_sucesso = request.session.pop('login_sucesso', False)
    fim_de_treino = request.session.pop('fim_de_treino', False)
    assinatura_feita = request.session.pop('assinatura_feita', False)

    context ={
        'exercicio': exercicio,
        'planos': planos,
        'cadastro_sucesso': cadastro_sucesso,
        'login_sucesso': login_sucesso,
        'fim_de_treino': fim_de_treino,
        'assinatura_feita': assinatura_feita
    }

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        context ={
            'exercicio': exercicio,
            'planos': planos,
            'pessoa': pessoa,
            'cadastro_sucesso': cadastro_sucesso,
            'login_sucesso': login_sucesso,
            'fim_de_treino': fim_de_treino,
            'assinatura_feita': assinatura_feita
        }
    
    return render(request, 'home.html', context)

def exercicios(request):
    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    context = {
        'exercicios': exercicios,
        'exercicios_count': exercicios_count,
    }

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        context = {
            'exercicios': exercicios,
            'exercicios_count': exercicios_count,
            'pessoa': pessoa
        }
    else:
        return redirect('erro')

        
    return render(request, 'exercicios.html', context)

def treinos(request):
    treinos = Treino.objects.filter(treino_do_buddy=1)
    context = {
        'treinos': treinos,
    }

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        context = {
        'treinos': treinos,
        'pessoa': pessoa,
    }
    else:
        return redirect('erro')
        
    return render(request, 'treinos.html', context)

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')

        # if senha1!=senha2:
        #     messages.error(request, 'Os campos de senha devem ser preenchidos com a mesma senha!')
        #     context={
        #         'nome': nome,
        #         'email': email,
        #         'senha1': senha1,
        #         'senha2': senha2
        #     }
        #     return render(request, 'cadastro.html', context)
        
        # if senha1=="" or senha2=="":
        #     messages.error(request, 'Insira uma senha!')
        #     context={
        #         'nome': nome,
        #         'email': email,
        #         'senha1': senha1,
        #         'senha2': senha2
        #     }
        #     return render(request, 'cadastro.html', context)
        
        if Pessoa.objects.filter(email=email).exists():
            messages.error(request, 'Esse email já existe!')
            context={
                'nome': nome,
                'email': email,
                'senha1': senha1,
                'senha2': senha2
            }
            return render(request, 'cadastro.html', context)
            
    
        pessoa = Pessoa(
            nome_usuario = nome,
            email=email,
            senha=make_password(senha1),
            id_plano = 4,
            id_perfil = 1
        )
        pessoa.save()
        request.session['pessoa_id'] = pessoa.idpessoa

        request.session['cadastro_sucesso'] = True
        return redirect('home')
    
    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            pessoa = Pessoa.objects.get(email=email)
            if check_password(senha, pessoa.senha):
                request.session['pessoa_id'] = pessoa.idpessoa
                request.session['login_sucesso'] = True
                return redirect('home')
            else:
                messages.error(request, 'Ops! Senha incorreta :(')

        except Pessoa.DoesNotExist:
            messages.error(request, 'Ops! Email não encontrado :(')
            return redirect('login')
    
    return render(request, 'login.html')


def logout(request):
    print("entrou na def logout")
    if request.method == 'POST':
        request.session.flush()
        print("Sessão encerrada. Redirecionando para home.")
        return redirect('home')
    else:
        return redirect('home')

def montagem_treinos(request):
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if pessoa.id_plano == 1 or pessoa.id_plano == 4:
            return redirect('erro')

        exercicios = Exercicios.objects.all()
        exercicios_count = exercicios.count()

        context = {
            'exercicios': exercicios,
            'exercicios_count': exercicios_count,
        }

        if request.method == "POST":
            acao = request.POST.get('acao')

            if acao == "selecionar":
                exercicios_ids = request.POST.getlist("exercicios_selecionados")
                if not exercicios_ids:
                    falta_ex = request.session["falta_ex"] = True
                    context={
                        'exercicios': exercicios,
                        'exercicios_count': exercicios_count,
                        'falta_ex': falta_ex
                    }
                    return render(request, 'montagemTreinos.html', context) 
                
                # Converte IDs para inteiros
                exercicios_ids = [int(ex_id) for ex_id in exercicios_ids if ex_id.isdigit()]
                exe_serie_rep = Exercicios.objects.filter(id_exercicios__in=exercicios_ids)

                context = {
                    'exercicios': exercicios,
                    'exercicios_count': exercicios_count,
                    'exercicios_ids': exercicios_ids,
                    'exe_serie_rep': exe_serie_rep
                }
                return render(request, 'montagemTreinos.html', context) 
            
            if acao == "salvar":
                exercicios_ids = request.POST.getlist("exercicios_selecionados")
                if not exercicios_ids:
                    falta_ex = request.session["falta_ex"] = True
                    context={
                        'exercicios': exercicios,
                        'exercicios_count': exercicios_count,
                        'falta_ex': falta_ex
                    }
                    return render(request, 'montagemTreinos.html', context) 
                exercicios_ids = [int(ex_id) for ex_id in exercicios_ids if ex_id.isdigit()]

                novo_treino = Treino.objects.create(
                    nome_treino = request.POST.get('nome'),
                    treino_do_buddy = 0
                )
                
                for ex_id in exercicios_ids:
                    valor_series = request.POST.get(f"series_{ex_id}")# esse f antes é pro python montar o nome da variável corretamente, 'somando' o id depois
                    valor_repeticoes = request.POST.get(f"repeticoes_{ex_id}")

                    RelTreinoExercicio.objects.create(
                        id_treino = novo_treino.id_treino,
                        id_exercicio = ex_id,
                        numero_repeticoes = int(valor_repeticoes), 
                        numero_series = int(valor_series),
                    )

                RelUsuarioTreino.objects.create(
                    id_pessoa = pessoa.idpessoa,
                    id_treino = novo_treino.id_treino
                )

                request.session['montagem_sucesso'] = True
                return redirect('meus_treinos')
            
    if not 'pessoa_id' in request.session:
        return redirect('erro')

    return render(request, 'montagemTreinos.html', context) 

def meus_treinos(request):
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if pessoa.id_plano == 1 or pessoa.id_plano == 4:
            return redirect('erro')

        rel_user_treino = RelUsuarioTreino.objects.filter(id_pessoa=pessoa.idpessoa)
        treinos = Treino.objects.filter(id_treino__in=[rel.id_treino for rel in rel_user_treino])
        context = {
            'treinos': treinos
        }

        if 'montagem_sucesso' in request.session:
            montagem_sucesso = request.session.pop('montagem_sucesso', False)
            context = {
                'treinos': treinos,
                'montagem_sucesso': montagem_sucesso
            }
    else:
        return redirect('erro')

    return render(request, 'meusTreinos.html', context)

def exercicio(request, pk):
    if 'pessoa_id' in request.session:
        exercicio = Exercicios.objects.get(id_exercicios=pk)
        rel_exercicios_musculos = RelExerciciosMusculos.objects.filter(id_exercicio=pk)
        musculos = MusculosEnvolvidos.objects.filter(id_musculos_envolvidos__in=[rel.id_musculo for rel in rel_exercicios_musculos])
        context={
            'exercicio': exercicio,
            'rel_exercicios_musculos': rel_exercicios_musculos,
            'musculos': musculos,
        }
    else:
        return redirect('erro')
    return render(request, 'pgExercicio.html', context)

def treino(request, pk):
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        treino = Treino.objects.get(id_treino=pk)
        rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=pk)
        exercicios = Exercicios.objects.filter(id_exercicios__in=[rel.id_exercicio for rel in rel_treino_exercicio])
        context={
            'treino': treino,
            'exercicios': exercicios,
            'rels': rel_treino_exercicio,
            'pessoa': pessoa
        }
        print([rel.id_exercicio for rel in rel_treino_exercicio])
        print([exercicio.id_exercicios for exercicio in exercicios])
    else:
        return redirect('erro')

    return render(request, 'pgTreino.html', context)


def treinoia(request,pk):

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if pessoa.id_plano == 3 or pessoa.id_plano == 4:
            return redirect('erro')

    if not 'pessoa_id' in request.session:
        return redirect('erro')

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
            request.session['fim_de_treino'] = True
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
                request.session['fim_de_treino'] = True
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
                    request.session['fim_de_treino'] = True
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

    if not 'pessoa_id' in request.session:
        return redirect('erro')

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
            request.session['fim_de_treino'] = True
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
                return redirect('treino_guiado', pk=pk)
            else:
                request.session.flush() # apaga tudo da session
                request.session['fim_de_treino'] = True
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
                    request.session['fim_de_treino'] = True
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

def pagamento(request, pk):
    if not 'pessoa_id' in request.session:
        return redirect('erro')

    plano = Plano.objects.get(id_plano=pk)
    context={
        'plano': plano,
    }

    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if request.method == 'POST':
            cpf = request.POST.get('cpf')
            mes = request.POST.get('data_mes')
            ano = request.POST.get('data_ano')
            data_validade = f"{mes.zfill(2)}/{ano}"
            CondPagamento.objects.create(
                numero_do_cartao = request.POST.get('numero_cartao'),
                nome = request.POST.get('nome'),
                id_plano = plano.id_plano,
                data_validade = data_validade,
                cvv = request.POST.get('cvv'),
            )
            pessoa.cpf = cpf
            pessoa.id_plano=plano.id_plano
            pessoa.save()
            request.session['assinatura_feita'] = True
            return redirect('home')
        
        context={
            'plano': plano,
            'pessoa': pessoa,
        }

    return render(request, "pagamento.html", context)

def erro(request):
    return render(request, "erro.html")