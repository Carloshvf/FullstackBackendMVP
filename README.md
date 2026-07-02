# Novels Shelf — Backend API

API REST para gerenciamento de um acervo pessoal de novels e livros. Permite cadastrar, buscar, atualizar e remover novels da base de dados, com documentação interativa via Swagger.

---

## Tecnologias utilizadas

- Python 3.9.6
- Flask + flask-openapi3
- SQLAlchemy + SQLite
- Pydantic
- Flask-CORS

---

## Estrutura do projeto

```
FullstackBackendMVP/
├── model/
│   ├── __init__.py       # Configuração do banco e sessão
│   ├── base.py           # Classe base do SQLAlchemy
│   └── novel.py          # Model da tabela novels
├── schemas/
│   ├── __init__.py       # Exportação dos schemas
│   ├── novel.py          # Schemas e funções de apresentação
│   └── error.py          # Schema de erros
├── database/             # Gerado automaticamente
├── log/                  # Gerado automaticamente
├── app.py                # Rotas da API
├── logger.py             # Configuração de logs
└── requirements.txt      # Dependências do projeto
```

---

## Instalação

### Pré-requisitos

- Python 3.9.6 instalado
- pip disponível no terminal

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/Carloshvf/FullstackBackendMVP.git
cd FullstackBackendMVP
```

**2. Crie e ative o ambiente virtual**

```bash
python -m venv .venv
```

Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Inicie o servidor**

```bash
flask run --host 0.0.0.0 --port 5000
```

Para desenvolvimento com reload automático:

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

A API estará disponível em `http://localhost:5000`.

---

## Documentação

Acesse `http://localhost:5000/` para ser redirecionado à documentação interativa via Swagger, onde é possível visualizar e testar todas as rotas disponíveis.

---

## Rotas disponíveis

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/novels` | Lista todas as novels cadastradas |
| `GET` | `/novel?titulo=` ou `/novel?autor=` | Busca uma novel por título ou autor |
| `POST` | `/novel` | Cadastra uma nova novel |
| `PATCH` | `/novel` | Atualiza score e/ou último capítulo |
| `DELETE` | `/novel?id=` | Remove uma novel pelo id |

---

## Campos da tabela novels

| Campo | Tipo | Obrigatório |
|---|---|---|
| `id` | Inteiro | Gerado automaticamente |
| `titulo` | Texto | Sim |
| `autor` | Texto | Sim |
| `genero` | Texto | Não |
| `sinopse` | Texto | Não |
| `score` | Decimal | Não |
| `ultimo_capitulo` | Inteiro | Não |
| `data_insercao` | Data/hora | Gerado automaticamente |
