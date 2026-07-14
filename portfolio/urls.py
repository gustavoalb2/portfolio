"""
URL configuration for portfolio project.
Admin URL é configurável via variável de ambiente ADMIN_URL_PATH.
O caminho padrão /admin/ é bloqueado para segurança.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import include, path


# Customização do AdminSite
admin.site.site_header = "Painel do Portfólio"
admin.site.site_title = "Administração"
admin.site.index_title = "Gerenciar Conteúdo do Site"

urlpatterns = [
    # Admin com URL customizada (via .env)
    path(settings.ADMIN_URL, admin.site.urls),

    # Bloqueio do caminho /admin/ padrão — retorna 404
    path('admin/', lambda request: HttpResponseNotFound(
        '<h1>404 — Página não encontrada</h1>'
    )),

    # Landing page pública
    path('', include('landing.urls')),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
