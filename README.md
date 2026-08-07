# Agência de Viagens - Sistema de Gerenciamento

## Introdução
Este projeto é uma aplicação de gerenciamento para uma agência de viagens fictícia, desenvolvida em Python. O principal foco do sistema é demonstrar a integração poliglota de persistência. Para isso, ele utiliza dois bancos de dados simultaneamente: o Supabase (PostgreSQL) para lidar com dados relacionais e transacionais (clientes, destinos e vendas), e o MongoDB Atlas (NoSQL) para o armazenamento flexível de comentários de clientes sobre as viagens. 

## Descrição das Interfaces
O sistema é composto por duas interfaces distintas que operam sobre a mesma base de dados, simulando cenários para diferentes tipos de usuários:

*   **Interface Web (Gradio):** Focada no fluxo de registro. Permite o cadastro sequencial de Clientes, Destinos e Vendas (salvos no Supabase) e, por fim, a inserção e visualização de Comentários das viagens (salvos no MongoDB). O sistema possui travas lógicas de validação, garantindo que um comentário só possa ser feito após a conclusão de uma venda.
*   **Interface Desktop (Tkinter):** Voltada para a administração do sistema. Oferece operações completas de CRUD (Create, Read, Update e Delete) para os dados estruturados no Supabase. A interface é separada por abas (Clientes, Destinos, Vendas), listando os registros em tabelas interativas e permitindo atualizações ou exclusões diretas com confirmação de segurança.

---

## Como Instalar e Executar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado (versão 3.8 ou superior). É altamente recomendável utilizar um ambiente virtual (`venv`).

### 2. Clonar e Preparar o Ambiente
No seu terminal, execute os comandos:
```bash
# Clone o repositório (substitua pela sua URL)
git clone [https://github.com/seu-usuario/agencia-viagens.git](https://github.com/seu-usuario/agencia-viagens.git)
cd agencia-viagens

# Crie e ative o ambiente virtual
python -m venv venv
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate

# Instale as dependências
pip install gradio supabase python-dotenv pymongo

```

### 3. Configurar as Variáveis de Ambiente

Na raiz do projeto, crie um arquivo chamado exatamente `.env` (ele será ignorado pelo Git graças ao `.gitignore`). Preencha-o com as suas credenciais do Supabase e do MongoDB Atlas:

```env
# ==========================================
# CREDENCIAIS SUPABASE (POSTGRESQL)
# ==========================================
URL_SUPABASE=sua_url_do_supabase_aqui
ANON_KEY=sua_anon_key_do_supabase_aqui

# ==========================================
# CREDENCIAIS MONGODB ATLAS (NOSQL)
# ==========================================
MONGODB_USERNAME=seu_usuario_do_mongo
MONGODB_PASSWORD=sua_senha_do_mongo
MONGODB_URI=sua_connection_string_do_mongo_aqui

```

*(Nota: Certifique-se de que o seu IP foi adicionado à "Network Access" no painel do MongoDB Atlas, preferencialmente `0.0.0.0/0` para testes locais).*

### 4. Executar as Aplicações

As duas interfaces funcionam de forma independente. Com o ambiente virtual ativado, escolha qual deseja rodar:

**Para iniciar a Interface Web (Gradio):**

```bash
python ui_web.py

```

*Acesse o link gerado no terminal (geralmente `http://127.0.0.1:7860`) no seu navegador.*

**Para iniciar a Interface Desktop (Tkinter):**

```bash
python desktop.py

```

*Uma janela nativa do seu sistema operacional será aberta com o painel de administração.*
