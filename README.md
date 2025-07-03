# Projeto Django - Toy Store

## Descrição

Este projeto é uma aplicação web completa para gestão de uma loja de brinquedos, desenvolvida com Django. O sistema
oferece autenticação de usuários, perfis personalizados com upload de foto, integração com redes sociais e uma API
robusta baseada em Django REST Framework.

A plataforma permite visualizar gráficos interativos de vendas, identificar clientes de destaque, acompanhar o
desempenho diário de vendas de brinquedos e consultar o valor total comercializado.

A API RESTful possibilita operações completas de cadastro, consulta, atualização e remoção (CRUD) de clientes e vendas,
facilitando integrações e automações.

O backoffice, acessível pelo admin do Django, proporciona uma interface eficiente para gerenciamento de vendas, clientes
e demais dados da loja.

Além disso, o projeto conta com um frontend intuitivo que consome a API e apresenta as informações de forma clara e
amigável, otimizando a experiência do usuário e a tomada de decisões gerenciais.

## Funcionalidades

- Cadastro, login e logout de usuários com autenticação segura
- Gerenciamento completo de clientes e vendas (CRUD)
- Edição de perfil de usuário, incluindo nome, data de nascimento e foto
- Autenticação por e-mail e senha para acesso ao frontend
- Autenticação via token para consumo da API RESTful
- Autenticação e gerenciamento de permissões no admin do Django
- Integração com redes sociais para login rápido (`social-auth`)
- Visualização de gráficos interativos de vendas e clientes em destaque
- Consulta do valor total de vendas e desempenho diário da loja
- API robusta baseada em Django REST Framework (endpoint `/api/v1/`)
- Banco de dados PostgreSQL gerenciado via Docker Compose
- Frontend intuitivo que consome a API e exibe dados de forma amigável

## Como rodar o projeto

1. **Clone o repositório e configure o `.env` com as variáveis do banco e do Google para autenticação do social auth:**

```bash
git clone
```

- Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

- Abra https://console.cloud.google.com/projectCreate no seu navegador. Para conseguir realizar o login com o Google,
  você precisa de uma chave de API do Google. Siga as instruções para criar um projeto e gerar as credenciais
  necessárias.

```plaintext
SECRET_KEY='change_this_to_your_secret_key'
DB_NAME=toy_store_db
DB_USER=root
DB_PASSWORD=root

GOOGLE_OAUTH2_KEY=change_this_to_your_google_oauth2_key
GOOGLE_OAUTH2_SECRET=change_this_to_your_google_oauth2_secret
```

2. **Suba os serviços com Docker Compose:**
   ```bash
   docker-compose up --build
    ```
3. **Acesse o admin do Django em `http://localhost:8000/admin` e crie um superusuário:**
4. **Acesse o frontend em `http://localhost:8000` e faça login com o superusuário criado ou se registre um novo usuário.
   **
5. **Acesse a API em `http://localhost:8000/api/v1/` para realizar operações CRUD de clientes e vendas.**
6. **Para acessar o backoffice, utilize o admin do Django em `http://localhost:8000/admin`.**
7. **Para visualizar os gráficos, acesse o frontend e navegue até o DashBoard.**

## Tecnologias Utilizadas

- Django
- Django REST Framework
- PostgreSQL
- Docker
- Python
- HTML/CSS/JavaScript
- Bootstrap
- Social Auth

