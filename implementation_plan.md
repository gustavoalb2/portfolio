# Deploy Portfólio na Vercel com Supabase

Este documento descreve o plano para adaptar o projeto Django existente para ser feito o deploy na Vercel, utilizando Supabase (Postgres gerenciado) para banco de dados e Supabase Storage (compatível com S3) para armazenamento de imagens.

## User Review Required

> [!WARNING]
> O ambiente serverless da Vercel (onde as funções abrem e fecham a todo momento) requer o uso de connection pooling com banco de dados relacionais. Usaremos a porta `6543` no endpoint do Supabase, que direciona para o PgBouncer interno do Supabase. Certifique-se de usar a porta correta na sua `DATABASE_URL`.

> [!IMPORTANT]
> Caso você já possua dados criados localmente no SQLite que deseje migrar para a produção, você deverá exportar os dados usando `dumpdata` **antes** de seguir com o deploy e importá-los com `loaddata` usando a URL do banco remoto.

## Proposed Changes

### Dependencies

#### [MODIFY] [requirements.txt](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/requirements.txt)
- Adicionar `dj-database-url` para parsing da URL de conexão do banco de dados (variável `DATABASE_URL`).
- Adicionar `psycopg2-binary` para comunicação com o PostgreSQL.
- Adicionar `django-storages[boto3]` para o suporte ao Supabase Storage (compatível com S3).
- Adicionar `whitenoise` para o gerenciamento de arquivos estáticos na Vercel.

### Settings Configuration

#### [MODIFY] [portfolio/settings.py](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/portfolio/settings.py)
- Importar e configurar o `dj_database_url` para sobrescrever as configurações de `DATABASES` se a variável `DATABASE_URL` existir (mantendo SQLite localmente se não existir).
- Configurar o `STORAGES` (ou `DEFAULT_FILE_STORAGE` / `STATICFILES_STORAGE` dependendo da versão do Django):
  - Em `DEBUG=True`, manter `FileSystemStorage` para os arquivos de media.
  - Em `DEBUG=False`, utilizar `storages.backends.s3.S3Storage` para enviar as imagens para o Supabase Storage.
- Atualizar a configuração `MIDDLEWARE` para incluir o `WhiteNoiseMiddleware` (necessário para servir arquivos estáticos em produção na Vercel).
- Configurar `CSRF_TRUSTED_ORIGINS` e atualizar `ALLOWED_HOSTS` a partir do `.env`.

### Environment Setup

#### [MODIFY] [.env.example](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/.env.example)
- Adicionar documentação e as chaves necessárias para:
  - Banco de dados (`DATABASE_URL`).
  - Storage (`SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY`, `SUPABASE_S3_BUCKET_NAME`, `SUPABASE_S3_ENDPOINT_URL`, `SUPABASE_S3_REGION_NAME`).
  - Vercel e Segurança (`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SECURE_SSL_REDIRECT`, etc).

### Vercel Configuration

#### [NEW] [vercel.json](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/vercel.json)
- Criar a configuração explicitando o entrypoint WSGI (`portfolio.wsgi.application`) ou usando a configuração recomendada da Vercel (geralmente apontando `builds` para o wsgi.py e mapeando a rota `/(.*)`).
- Adicionar script para coleta de estáticos e migrações no build se necessário (geralmente executado no comando build `build_files.sh` ou similar).

#### [NEW] [build_files.sh](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/build_files.sh) (Opcional, mas recomendado na Vercel)
- Script de build simples para instalar as dependências e rodar `python manage.py collectstatic`. A Vercel prefere rodar um script customizado para projetos Django.

### Walkthrough & Checklist de Deploy

- Como a configuração da Vercel e do Supabase envolve passos fora do código-fonte (Painel Supabase, Painel Vercel), vou incluir no Walkthrough o passo a passo exato.

## Verification Plan

### Automated Tests
- N/A para esta alteração, pois não temos suíte de testes customizada.

### Manual Verification
1. Configurar Supabase e obter variáveis.
2. Fazer Deploy na Vercel e configurar as variáveis no dashboard da Vercel.
3. Testar a interface de administração na Vercel criando/editando itens.
4. Fazer upload de imagem via Admin da Vercel e verificar se ela é servida corretamente a partir da URL do bucket Supabase S3 na Landing Page pública.
