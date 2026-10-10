from decimal import Decimal

from .models import Produto

CART_SESSION_KEY = "carrinho"


class Carrinho:
    """Carrinho simples guardado na sessão do Django."""

    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(CART_SESSION_KEY)
        if carrinho is None:
            carrinho = self.session[CART_SESSION_KEY] = {}
        self.carrinho = carrinho

    def adicionar(self, produto, quantidade=1):
        produto_id = str(produto.id)
        if produto_id not in self.carrinho:
            self.carrinho[produto_id] = {
                "quantidade": 0,
                "preco": str(produto.preco),
            }
        self.carrinho[produto_id]["quantidade"] += quantidade
        self.salvar()

    def remover(self, produto):
        produto_id = str(produto.id)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
            self.salvar()

    def limpar(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.modified = True

    def salvar(self):
        self.session[CART_SESSION_KEY] = self.carrinho
        self.session.modified = True

    def __iter__(self):
        ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=ids)
        produtos_map = {str(p.id): p for p in produtos}

        for produto_id, item in self.carrinho.items():
            produto = produtos_map.get(produto_id)
            if not produto:
                continue
            preco = Decimal(item["preco"])
            quantidade = item["quantidade"]
            yield {
                "produto": produto,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": preco * quantidade,
            }

    def __len__(self):
        return sum(item["quantidade"] for item in self.carrinho.values())

    def __bool__(self):
        return len(self) > 0

    @property
    def total(self):
        return sum(
            (Decimal(item["preco"]) * item["quantidade"] for item in self.carrinho.values()),
            Decimal("0.00"),
        )
