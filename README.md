# Estudos Django

Projeto base com **blog**, **loja (e-commerce)** e **ChatBot integrado ao Ollama** no mesmo site.

## Estrutura

| Pasta / arquivo | Função |
|---|---|
| `config/` | Configuração do projeto |
| `blog/` | App de posts |
| `loja/` | App de e-commerce (produtos, carrinho, pedidos) |
| `chatbot/` | ChatBot que fala com o Ollama local |
| `templates/` | HTML compartilhado e por app |
| `manage.py` | Comandos do Django |

## URLs principais

- `/` — home (produtos + posts)
- `/loja/` — listagem de produtos
- `/loja/carrinho/` — carrinho (sessão)
- `/loja/checkout/` — finalizar pedido
- `/blog/` — listagem de posts
- `/chatbot/` — ChatBot com seletor de modelo Ollama
- `/admin/` — painel administrativo

## Como rodar

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
  - usuário: `admin`
  - senha: `admin123`

## ChatBot + Ollama

O app `chatbot` lista os modelos instalados no seu Ollama e permite conversar escolhendo qual modelo usar.

### Pré-requisitos

1. Ollama instalado e em execução
2. Pelo menos um modelo baixado, por exemplo:

```powershell
ollama list
ollama pull qwen2.5-coder:14b
```

### Como usar

1. Suba o Django (`python manage.py runserver`)
2. Abra http://127.0.0.1:8000/chatbot/
3. Selecione o modelo no dropdown
4. Envie mensagens — o histórico fica na sessão do navegador
5. Use **Limpar conversa** para recomeçar

### O que o app faz

- Consulta `GET /api/tags` do Ollama para montar a lista de modelos
- Envia o histórico para `POST /api/chat` com o modelo escolhido
- Endpoints internos:
  - `/chatbot/` — interface do chat
  - `/chatbot/api/modelos/` — lista modelos
  - `/chatbot/api/enviar/` — envia mensagem
  - `/chatbot/api/limpar/` — limpa histórico

### Configuração

Em `config/settings.py`:

| Setting | Padrão | Função |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | URL da API do Ollama |
| `OLLAMA_TIMEOUT` | `300` | Timeout em segundos (modelos grandes podem demorar) |

## Fluxo da loja

1. Produto cadastrado no admin (`Produto` / `Categoria`)
2. Visitante adiciona ao **carrinho** (salvo na sessão)
3. Checkout cria um **Pedido** + **ItemPedido**
4. Pedido aparece no admin para acompanhar o status
