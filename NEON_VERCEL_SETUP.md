# Configuração do Neon DB com Vercel

## Informações do Projeto Neon

- **Project ID**: `sparkling-band-99137932`
- **Branch**: `main` (ID: `br-rapid-rice-atcgcig3`)
- **Database**: `neondb`
- **Role**: `neondb_owner`

## Passo 1: Clonar o .env.example

Localmente, renomeie `.env.example` para `.env` e atualize com suas variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas variáveis específicas.

## Passo 2: Configurar no Vercel

### Via CLI:

```bash
vercel env add DATABASE_URL
# Cole a connection string quando solicitado
```

### Via Dashboard Vercel:

1. Vá para seu projeto no [Dashboard do Vercel](https://vercel.com)
2. Clique em **Settings** → **Environment Variables**
3. Adicione as seguintes variáveis:

| Variável | Valor |
|----------|-------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_pRwD32UJMPsV@ep-square-cake-ats7rz2n-pooler.c-9.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require` |
| `SECRET_KEY` | Gere com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `VERCEL` | `True` |
| `ALLOWED_HOSTS` | `seu-dominio.vercel.app,www.seu-dominio.vercel.app` |
| `ADMIN_URL_PATH` | `painel-secreto/` (ou qualquer outra URL) |

## Passo 3: Testes Locais

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute as migrations:
```bash
python manage.py migrate
```

3. Crie um superuser:
```bash
python manage.py createsuperuser
```

4. Teste localmente:
```bash
python manage.py runserver
```

## Passo 4: Deploy no Vercel

1. Faça commit e push:
```bash
git add .
git commit -m "Add Neon DB configuration"
git push
```

2. O Vercel fará deploy automaticamente e executará o `build.sh`, que:
   - Executa migrações: `python manage.py migrate --noinput`
   - Coleta arquivos estáticos: `python manage.py collectstatic --noinput`

## Troubleshooting

### Erro de conexão com o banco de dados:
- Verifique se a `DATABASE_URL` está corretamente definida no Vercel
- Verifique se o `psycopg[binary]` está instalado (já está no requirements.txt)

### Erro de arquivos estáticos:
- O `whitenoise` já está configurado para servir arquivos estáticos
- Certifique-se de que `whitenoise.middleware.WhiteNoiseMiddleware` está no middleware

### Erro de migrations:
- Se houver erro nas migrations, verifique os logs no Vercel dashboard
- Você pode executar migrations manualmente acessando a página do Vercel

## Variáveis de Ambiente Recomendadas

Adicione também essas variáveis recomendadas no Vercel:

```
CSRF_TRUSTED_ORIGINS=https://seu-dominio.vercel.app
```

## Backup do Banco de Dados

Para fazer backup do seu banco de dados Neon:

```bash
pg_dump "postgresql://neondb_owner:npg_pRwD32UJMPsV@ep-square-cake-ats7rz2n-pooler.c-9.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require" > backup.sql
```

## Recursos Úteis

- [Documentação do Neon](https://neon.tech/docs)
- [Documentação do Vercel para Django](https://vercel.com/guides/deploying-django-with-vercel)
- [Documentação do Django com PostgreSQL](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
