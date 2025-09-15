"""
URL configuration for tb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tb_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('pagamento/<int:pk>', views.pagamento, name='pagamento'),

    path('exercicios/', views.exercicios, name='exercicios'),
    path('exercicio/<int:pk>', views.exercicio, name='exercicio'),

    path('treinos/', views.treinos, name='treinos'),
    path('treino/<int:pk>', views.treino, name='treino'),
    path('treinoia/<int:pk>', views.treinoia, name='treinoia'),
    path('treino_guiado/<int:pk>', views.treino_guiado, name='treino_guiado'),

    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('montagem_treinos/', views.montagem_treinos, name='montagem_treinos'),
    path('editar_treino/<int:pk>', views.editar_treino, name="editar_treino"),
    path('meus_treinos/', views.meus_treinos, name='meus_treinos'),

    path('erro/', views.erro, name='erro'),

    path('recuperar_senha/', views.recuperar_senha, name='recuperar_senha'),
    # formulário para nova senha (link enviado por e-mail)
    path('redefinicao_de_senha/<uidb64>/<token>/', views.trocar_senha, name='redefinicao_de_senha'),

    # 4️⃣ Página final de senha redefinida com sucesso
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
