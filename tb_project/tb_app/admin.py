from django.contrib import admin
from .models import Perfil, Pessoa, Plano, CondPagamento, Treino, Exercicios, ErrosPossiveis, NivelDificuldade


admin.site.register(Perfil)
admin.site.register(Pessoa)
admin.site.register(Plano)
admin.site.register(CondPagamento)
admin.site.register(Treino)
admin.site.register(Exercicios)
admin.site.register(ErrosPossiveis)
admin.site.register(NivelDificuldade)