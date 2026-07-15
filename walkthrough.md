# Guia de Deploy na Vercel com Supabase

O projeto foi adaptado para ser hospedado na Vercel com o banco de dados e os arquivos estáticos gerenciados pelo Supabase. Abaixo estão os passos exatos para colocar tudo no ar:

## 1. Configurando o Banco de Dados no Supabase (Postgres)
1. Crie uma conta/projeto no [Supabase](https://supabase.com/).
2. Ao criar o projeto, anote a **Senha do Banco de Dados** (Database Password).
3. Vá em **Project Settings > Database**.
4. Desça até a seção **Connection String** e escolha a aba **URI**.
5. Certifique-se de que a opção **Use connection pooling** está ativa (porta `6543`). O Supabase usa PgBouncer, que é mandatório para Serverless Functions (como na Vercel) para não esgotar as conexões do banco.
6. Copie a string de conexão que deve se parecer com:
   `postgresql://postgres.[sua-ref]:[SUA_SENHA]@aws-0-[regiao].pooler.supabase.com:6543/postgres`
7. Esta será a sua `DATABASE_URL` na Vercel.

## 2. Configurando o Storage no Supabase (Imagens)
1. No painel do Supabase, vá na seção **Storage** e crie um novo bucket chamado `portfolio-media`.
2. Configure o bucket como **Public**.
3. Crie uma política de acesso para permitir inserção/deleção (opcional para admin, mas você fará isso pelo Django) ou simplesmente vá em **Storage > S3 Connection**.
4. Copie os seguintes dados:
   - **Endpoint URL**: `https://[sua-ref].supabase.co/storage/v1/s3`
   - **Access Key**
   - **Secret Key**
   - **Region**: `auto` (ou a região do seu projeto).
5. Estas serão as chaves `SUPABASE_S3_*` no `.env` da Vercel.

## 3. Realizando o Deploy na Vercel
1. Tenha todo o seu código na branch principal do GitHub.
2. Acesse a [Vercel](https://vercel.com/) e clique em **Add New Project**.
3. Importe o repositório do seu Portfólio.
4. Antes de clicar em Deploy, expanda a seção **Environment Variables** e adicione TODAS as variáveis documentadas no seu arquivo [`.env.example`](file:///d:/Users/Gustavo/Documents/GitHub/portfolio/.env.example):
   - `SECRET_KEY`
   - `DEBUG` (configure para `False`)
   - `ALLOWED_HOSTS` (ex: `.vercel.app,seu-dominio.com`)
   - `CSRF_TRUSTED_ORIGINS` (ex: `https://*.vercel.app,https://seu-dominio.com`)
   - `DATABASE_URL`
   - `ADMIN_URL_PATH` (escolha um caminho difícil de adivinhar, ex: `admin-secreto/`)
   - `SUPABASE_S3_ACCESS_KEY_ID`
   - `SUPABASE_S3_SECRET_ACCESS_KEY`
   - `SUPABASE_S3_BUCKET_NAME` (ex: `portfolio-media`)
   - `SUPABASE_S3_ENDPOINT_URL`
   - `SUPABASE_S3_REGION_NAME`
5. Clique em **Deploy**. A Vercel executará o arquivo `build_files.sh` e fará o setup.

> [!CAUTION]
> Lembre-se de configurar `DEBUG=False` para segurança em produção!

## 4. Migrações e Superusuário
Como a Vercel é Serverless e não tem terminal contínuo, as migrações não ocorrem automaticamente da mesma forma que localmente (embora não tenhamos incluído migrações no script de build para evitar race conditions em cada deploy). 
Você deve aplicar as migrações remotamente a partir da sua máquina local:

1. No seu terminal local, exporte a variável `DATABASE_URL` para o banco de produção:
   - No Windows (PowerShell): `$env:DATABASE_URL="sua-url-do-supabase"`
   - No Linux/Mac: `export DATABASE_URL="sua-url-do-supabase"`
2. Aplique as migrações no banco remoto: `python manage.py migrate`
3. Crie o superusuário remotamente: `python manage.py createsuperuser`
4. (Opcional) Caso você tenha dados em seu SQLite local, você pode exportar e importar para a produção:
   - Exportando: `python manage.py dumpdata > backup.json`
   - Mudando o `.env` (ou export de variável) para o banco remoto e importando: `python manage.py loaddata backup.json`

## 5. Checklist de Validação Pós-Deploy
Após o deploy ter sucesso, verifique:
1. **Página Principal**: A landing page deve carregar perfeitamente. O CSS deve estar presente (os arquivos estáticos foram compilados via WhiteNoise).
2. **Admin**: Acesse a URL `https://seu-projeto.vercel.app/ADMIN_URL_PATH/` para logar no sistema.
3. **Upload de Mídia**: Teste enviar uma imagem via painel de administração (ex: foto de uma experiência ou skill). Salve.
4. **Verificação de Mídia**: Confira na página principal se a imagem carrega normalmente e clique nela (ou inspecione com o botão direito) para verificar a URL: ela deve apontar para a URL pública do seu bucket Supabase S3 e não para um diretório local da Vercel.
5. **Persistência**: Ao fazer um novo deploy na Vercel (push no repositório), os dados do banco continuarão existindo (prova de que o PostgreSQL está sendo usado no lugar do SQLite local).
