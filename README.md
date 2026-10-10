# Estudos Django

Projeto base com **blog** e **loja (e-commerce)** no mesmo site.

## Estrutura

| Pasta / arquivo | Função |
|---|---|
| `config/` | Configuração do projeto |
| `blog/` | App de posts |
| `loja/` | App de e-commerce (produtos, carrinho, pedidos) |
| `templates/` | HTML compartilhado e por app |
| `manage.py` | Comandos do Django |

## URLs principais

- `/` — home (produtos + posts)
- `/loja/` — listagem de produtos
- `/loja/carrinho/` — carrinho (sessão)
- `/loja/checkout/` — finalizar pedido
- `/blog/` — listagem de posts
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

## Fluxo da loja

1. Produto cadastrado no admin (`Produto` / `Categoria`)
2. Visitante adiciona ao **carrinho** (salvo na sessão)
3. Checkout cria um **Pedido** + **ItemPedido**
4. Pedido aparece no admin para acompanhar o status
