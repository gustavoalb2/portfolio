# ☁️ Configuração do Cloudinary para Upload de Imagens

## 🤔 Por que Cloudinary?

O Vercel usa um **sistema de arquivos read-only**, então você não pode salvar arquivos localmente em produção. O Cloudinary é uma solução simples e gratuita para armazenar imagens na nuvem.

---

## 🚀 Setup Rápido (5 minutos)

### 1️⃣ Crie uma conta no Cloudinary

1. Acesse [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)
2. Crie uma conta gratuita (free tier é mais que suficiente)
3. Você receberá um email de confirmação

### 2️⃣ Obtenha suas credenciais

1. Após fazer login, vá para o [Dashboard](https://cloudinary.com/console)
2. Na seção "Account Details", você verá:
   - **Cloud Name** (ex: `dj7x1ql9v`)
   - **API Key** (ex: `123456789012345`)
   - **API Secret** (ex: `abcDEF1234ghiJKL5678`)

### 3️⃣ Configure localmente (desenvolvimento)

1. Abra o `.env` local:

```bash
# Cloudinary
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret
VERCEL=False
```

2. Instale os pacotes:

```bash
pip install -r requirements.txt
```

3. Teste:

```bash
python manage.py runserver
# Visite http://localhost:8000/painel-secreto/
# Tente fazer upload de uma imagem
```

### 4️⃣ Configure no Vercel (produção)

1. Vá para seu projeto no [Vercel Dashboard](https://vercel.com)
2. Clique em **Settings** → **Environment Variables**
3. Adicione as 3 variáveis:

| Variável | Valor |
|----------|-------|
| `CLOUDINARY_CLOUD_NAME` | (seu cloud name) |
| `CLOUDINARY_API_KEY` | (sua api key) |
| `CLOUDINARY_API_SECRET` | (seu api secret) |

4. Redeploy:

```bash
git add .
git commit -m "Add Cloudinary storage for image uploads"
git push
```

---

## 📸 Como Funciona

- **Desenvolvimento**: Imagens são salvas em `media/` localmente
- **Produção (Vercel)**: Imagens são enviadas automaticamente para Cloudinary
- **URL das imagens**: Serão servidas via CDN do Cloudinary (muito rápido!)

---

## 🎯 Funcionalidades do Cloudinary Free Tier

- ✅ 25 GB de armazenamento
- ✅ 25 GB de bandwidth/mês
- ✅ API completa
- ✅ CDN global
- ✅ Transformações de imagem (resize, crop, etc.)
- ✅ Sem limite de imagens

---

## ⚙️ Configuração Técnica

O arquivo `settings.py` foi atualizado com lógica condicional:

```python
if IS_VERCEL and CLOUDINARY_CLOUD_NAME:
    # Usa Cloudinary em produção
    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        ...
    }
else:
    # Usa FileSystem local em desenvolvimento
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            ...
        },
        ...
    }
```

---

## 🆘 Troubleshooting

### Erro: "Could not find config for 'default'"

Verifique se as variáveis de ambiente estão configuradas:

```bash
# Localmente
echo $CLOUDINARY_CLOUD_NAME

# No Vercel
# Clique no projeto → Settings → Environment Variables
```

### Erro: "Invalid Cloud Name"

Verifique se o `CLOUDINARY_CLOUD_NAME` está correto no `.env`

### Imagens não aparecem

1. Verifique se o upload foi bem-sucedido (no admin)
2. Confirme que as credenciais estão corretas
3. Verifique se está com acesso à internet

---

## 📚 Recursos Adicionais

- [Documentação Cloudinary](https://cloudinary.com/documentation)
- [Django Cloudinary Storage](https://github.com/klis87/django-cloudinary-storage)
- [Transformações de Imagem](https://cloudinary.com/documentation/image_transformations)

---

## ✅ Próximos Passos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Testar localmente
python manage.py runserver

# 3. Deploy
git add .
git commit -m "Add Cloudinary configuration"
git push

# 4. Configure no Vercel Dashboard
# (veja passo 4️⃣ acima)

# 5. Teste no Vercel
# Visite seu domínio no Vercel e teste upload de imagens
```

Tudo pronto! Agora você pode fazer upload de imagens sem problemas! 🎉
