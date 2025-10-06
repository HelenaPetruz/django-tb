from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
import random
from django.contrib import messages
from .models import Exercicios, Treino, NivelDificuldade, MusculosEnvolvidos, RelExerciciosMusculos, Plano, RelTreinoExercicio, ErrosPossiveis, CondPagamento, Pessoa, RelUsuarioTreino, TreinosSalvos
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.core import signing
from validate_docbr import CPF

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
    senha_redefinida_sucesso = request.session.pop('senha_redefinida_sucesso', False)

    context ={
        'exercicio': exercicio,
        'planos': planos,
        'cadastro_sucesso': cadastro_sucesso,
        'login_sucesso': login_sucesso,
        'fim_de_treino': fim_de_treino,
        'assinatura_feita': assinatura_feita,
        'senha_redefinida_sucesso': senha_redefinida_sucesso,
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
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])
        niveis = NivelDificuldade.objects.all()
        musculos = MusculosEnvolvidos.objects.all()
        niveis_selecionados = request.GET.getlist('q_niveis')
        musculos_selecionados = request.GET.getlist('q_musculos')

        treinos_query = Treino.objects.filter(treino_do_buddy=1)
        exercicios = Exercicios.objects.all()

        if niveis_selecionados:
            exercicios = exercicios.filter(id_nivel_dificuldade__in = niveis_selecionados)

        if musculos_selecionados:
            exercicios_ids_com_musculos = RelExerciciosMusculos.objects.filter(
                id_musculo__in=musculos_selecionados
            ).values_list('id_exercicio', flat=True) 
            # a funcao .values_list cria uma lista apenas com o parametro passado, nesse caso o id dos exercicios
            # e o flat=true é só quando a lista pega apenas 1 campo

            exercicios = exercicios.filter(id_exercicios__in=exercicios_ids_com_musculos)

        rel_treinos = RelTreinoExercicio.objects.filter(
            id_exercicio__in=exercicios.values_list('id_exercicios', flat=True)
        ).values_list('id_treino', flat=True)

        treinos = treinos_query.filter(id_treino__in=rel_treinos).distinct()

        treino_salvo = False
        erro_treino_salvo = False
        assinatura_necessaria = False
        if request.method == 'POST':
            if pessoa.id_plano==4:
                assinatura_necessaria = True
            else:
                id_user = pessoa.idpessoa
                id_treino = request.POST.get('salvar')

                existe = TreinosSalvos.objects.filter(id_treino_do_buddy=id_treino, id_pessoa=id_user).exists()
                if existe:
                    erro_treino_salvo = True
                else:
                    TreinosSalvos.objects.create(
                        id_pessoa = pessoa.idpessoa,
                        id_treino_do_buddy = request.POST.get('salvar')
                    )
                    treino_salvo = True

        context = {
            'treinos': treinos,
            'pessoa': pessoa,
            'niveis': niveis,
            'musculos': musculos,
            'niveis_selecionados': list(map(int,niveis_selecionados)),
            'musculos_selecionados': list(map(int,musculos_selecionados)),
            'treino_salvo': treino_salvo,
            'erro_treino_salvo': erro_treino_salvo,
            'assinatura_necessaria': assinatura_necessaria
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

        if Pessoa.objects.filter(email=email).exists():
            messages.error(request, 'Esse email já existe!')
            context={
                'nome': nome,
                'email': email,
                'senha1': senha1,
                'senha2': senha2
            } 
            return render(request, 'cadastro.html', context)
            
        if senha1 == senha2:
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
        else:
            messages.error(request, 'Insira a mesma senha nos campos!')
            return render(request, 'cadastro.html')
    
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
    
def gerar_token(pessoa_id):
    return signing.dumps({"id": pessoa_id})

def validar_token(token):
    try:
        data = signing.loads(token, max_age=3600)  # expira em 1h
        return data["id"]
    except signing.BadSignature:
        return None

def recuperar_senha(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            pessoa = Pessoa.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(pessoa.idpessoa))
            token = gerar_token(pessoa.idpessoa)
            link = request.build_absolute_uri(f"/redefinicao_de_senha/{uid}/{token}/")
            asssunto = "Trainer Buddy: Redefinição de senha"
            mensagem = f"Olá {pessoa.nome_usuario},\n\nClique no link abaixo para redefinir sua senha:\n{link}"
            send_mail(asssunto, mensagem, settings.DEFAULT_FROM_EMAIL, [pessoa.email])
            messages.success(request, 'E-mail enviado com sucesso! :)')

        except Pessoa.DoesNotExist:
            messages.error(request, 'Ops! Email não encontrado :(')
            # return render(request, "recuperar_senha.html", {"error": "E-mail não encontrado!"})

    return render(request, "recuperar_senha.html")

def trocar_senha(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print("ID DA PESSOA: ", uid)
        pessoa = Pessoa.objects.get(idpessoa=uid)
    except (TypeError, ValueError, OverflowError, pessoa.DoesNotExist):
        pessoa = None

    pessoa_id = validar_token(token)
    if pessoa_id and pessoa is not None:
        if request.method == "POST":
            nova_senha1 = request.POST.get("senha1")
            nova_senha2 = request.POST.get("senha2")
            if nova_senha1 == nova_senha2:
                if not check_password(nova_senha1, pessoa.senha):
                    pessoa.senha = make_password(nova_senha1)
                    pessoa.save()
                    request.session['senha_redefinida_sucesso'] = True
                    return redirect('home')
                else:
                    messages.error(request, 'A nova senha não pode ser igual a anterior :(')
            else:
                messages.error(request, 'Insira a mesma senha nos campos!')
        return render(request, "trocar_senha.html")
    else: # token inválido ou expirado
        return render(request, "trocar_senha.html", {"error": "Usuário não encontrado!"})


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
            'pagina': "criar",
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
                        'falta_ex': falta_ex,
                        'pagina': "criar",
                    }
                    return render(request, 'montagemTreinos.html', context) 
                
                # Converte IDs para inteiros
                exercicios_ids = [int(ex_id) for ex_id in exercicios_ids if ex_id.isdigit()]
                exe_serie_rep = Exercicios.objects.filter(id_exercicios__in=exercicios_ids)

                context = {
                    'exercicios': exercicios,
                    'exercicios_count': exercicios_count,
                    'exercicios_ids': exercicios_ids,
                    'exe_serie_rep': exe_serie_rep,
                    'pagina': "criar",
                }
                return render(request, 'montagemTreinos.html', context) 
            
            if acao == "salvar":
                exercicios_ids = request.POST.getlist("exercicios_selecionados")
                if not exercicios_ids:
                    falta_ex = request.session["falta_ex"] = True
                    context={
                        'exercicios': exercicios,
                        'exercicios_count': exercicios_count,
                        'falta_ex': falta_ex,
                        'pagina': "criar",
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

def editar_treino(request, pk):
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if pessoa.id_plano == 1 or pessoa.id_plano == 4:
            return redirect('erro')
        if not 'pessoa_id' in request.session:
            return redirect('erro')
        
    treino = Treino.objects.get(id_treino = pk)
    relacoes = RelTreinoExercicio.objects.filter(id_treino=treino.id_treino)
    exercicios_ids = [rel.id_exercicio for rel in relacoes] #exercícios selecionados
    exercicios = Exercicios.objects.all()
    exercicios_count = exercicios.count()
    exe_serie_rep = []
    for rel in relacoes:
        ex = Exercicios.objects.get(id_exercicios=rel.id_exercicio)
        ex.series = rel.numero_series
        ex.repeticoes = rel.numero_repeticoes
        exe_serie_rep.append(ex)

    context = {
        'pagina': "editar",
        'nome': treino.nome_treino,
        'exercicios': exercicios,
        'exercicios_count': exercicios_count,
        'exercicios_ids': exercicios_ids,   # marcar os checkboxes
        'exe_serie_rep': exe_serie_rep,     # para séries/repeticoes
        'treino_id': treino.id_treino,
    }

    if request.method == "POST":
        acao = request.POST.get('acao')

        if acao == "selecionar":
            exercicios_ids = [int(ex_id) for ex_id in request.POST.getlist("exercicios_selecionados") if ex_id.isdigit()]
            exe_serie_rep = Exercicios.objects.filter(id_exercicios__in=exercicios_ids)

            context.update({
                'exercicios_ids': exercicios_ids,
                'exe_serie_rep': exe_serie_rep,
            })
            return render(request, 'montagemTreinos.html', context)

        if acao == "salvar":
            exercicios_ids = [int(ex_id) for ex_id in request.POST.getlist("exercicios_selecionados") if ex_id.isdigit()]
            if not exercicios_ids:
                context['falta_ex'] = True
                return render(request, 'montagemTreinos.html', context)

            treino.nome_treino = request.POST.get('nome')
            treino.save()

            RelTreinoExercicio.objects.filter(id_treino=treino.id_treino).delete()
            for ex_id in exercicios_ids:
                valor_series = request.POST.get(f"series_{ex_id}")
                valor_repeticoes = request.POST.get(f"repeticoes_{ex_id}")
                RelTreinoExercicio.objects.create(
                    id_treino=treino.id_treino,
                    id_exercicio=ex_id,
                    numero_series=int(valor_series),
                    numero_repeticoes=int(valor_repeticoes),
                )

            request.session['edicao_sucesso'] = True
            return redirect('meus_treinos')
    return render(request, 'montagemTreinos.html', context) 

def meus_treinos(request):
    if 'pessoa_id' in request.session:
        pessoa = Pessoa.objects.get(idpessoa=request.session['pessoa_id'])

        if pessoa.id_plano == 4:
            return redirect('erro')

        treinos_salvos = ""
        rel_user_treino = RelUsuarioTreino.objects.filter(id_pessoa=pessoa.idpessoa)
        treinos = Treino.objects.filter(id_treino__in=[rel.id_treino for rel in rel_user_treino])

        rel_treinos_salvos = TreinosSalvos.objects.filter(id_pessoa=pessoa.idpessoa).values_list('id_treino_do_buddy', flat=True) 
        treinos_salvos = Treino.objects.filter(id_treino__in = rel_treinos_salvos)
        context = {
            'treinos': treinos,
            'treinos_salvos': treinos_salvos
        }

        if 'montagem_sucesso' in request.session:
            montagem_sucesso = request.session.pop('montagem_sucesso', False)
            context = {
                'treinos': treinos,
                'montagem_sucesso': montagem_sucesso,
                'treinos_salvos': treinos_salvos
            }

        if 'edicao_sucesso' in request.session:
            edicao_sucesso = request.session.pop('edicao_sucesso', False)
            context = {
                'treinos': treinos,
                'edicao_sucesso': edicao_sucesso,
                'treinos_salvos': treinos_salvos
            }

        if request.method == 'POST':
            id_treino = request.POST.get('excluir_treino')
            print("ID: ", id_treino)
            treino = Treino.objects.get(id_treino= id_treino)
            if treino.treino_do_buddy == False:
                rel_treino_exercicio = RelTreinoExercicio.objects.filter(id_treino=id_treino)
                rel_user_treino = RelUsuarioTreino.objects.filter(id_treino=id_treino)
                treino.delete()
                rel_treino_exercicio.delete()
                rel_user_treino.delete()
            else:
                treino_salvo = TreinosSalvos.objects.filter(id_treino_do_buddy=id_treino, id_pessoa=pessoa.idpessoa)
                treino_salvo.delete()


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

        treino_salvo = False
        erro_treino_salvo = False
        assinatura_necessaria = False
        if request.method == 'POST':
            if pessoa.id_plano==4:
                assinatura_necessaria = True
            else:
                id_user = pessoa.idpessoa
                id_treino = request.POST.get('salvar')

                existe = TreinosSalvos.objects.filter(id_treino_do_buddy=id_treino, id_pessoa=id_user).exists()
                if existe:
                    erro_treino_salvo = True
                else:
                    TreinosSalvos.objects.create(
                        id_pessoa = pessoa.idpessoa,
                        id_treino_do_buddy = request.POST.get('salvar')
                    )
                    treino_salvo = True

        context={
            'treino': treino,
            'exercicios': exercicios,
            'rels': rel_treino_exercicio,
            'pessoa': pessoa,
            'treino_salvo': treino_salvo,
            'erro_treino_salvo': erro_treino_salvo,
            'assinatura_necessaria': assinatura_necessaria
        }

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
                request.session.pop('indice', None)
                request.session.pop('serie_atual', None)
                request.session.pop('mostrar_descanso', None)
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
                    request.session.pop('indice', None)
                    request.session.pop('serie_atual', None)
                    request.session.pop('mostrar_descanso', None)
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
            else: # apaga tudo da session
                request.session.pop('indice', None)
                request.session.pop('serie_atual', None)
                request.session.pop('mostrar_descanso', None) 
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
                    request.session.pop('indice', None)# apaga tudo da session
                    request.session.pop('serie_atual', None)
                    request.session.pop('mostrar_descanso', None)    
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
            numero_do_cartao = request.POST.get('numero_cartao')
            nome = request.POST.get('nome')
            cvv = request.POST.get('cvv')
            validador = CPF()
            if not validador.validate(cpf):
                print('CPF INVALIDO')
                context={
                    'plano': plano,
                    'pessoa': pessoa,
                    'cpf': cpf,
                    'mes': mes,
                    'ano':ano,
                    'numero': numero_do_cartao,
                    'nome': nome,
                    'cvv': cvv,
                    'cpf_invalido': True
                }
                return render(request, "pagamento.html", context)
                # return redirect('pagamento', pk)
            CondPagamento.objects.create(
                numero_do_cartao = numero_do_cartao,
                nome = nome,
                id_plano = plano.id_plano,
                data_validade = data_validade,
                cvv = cvv
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