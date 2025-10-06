from django.contrib import admin
from .models import Perfil, Pessoa, Plano, CondPagamento, Treino, Exercicios, NivelDificuldade, RelExerciciosMusculos, RelPlanoTreino, RelTreinoExercicio, MusculosEnvolvidos


admin.site.register(Perfil)
admin.site.register(Pessoa)
admin.site.register(Plano)
admin.site.register(CondPagamento)
admin.site.register(Treino)
admin.site.register(Exercicios)
admin.site.register(NivelDificuldade)
admin.site.register(RelExerciciosMusculos)
admin.site.register(RelPlanoTreino)
admin.site.register(RelTreinoExercicio)
admin.site.register(MusculosEnvolvidos)