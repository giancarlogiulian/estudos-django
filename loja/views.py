from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from blog.models import Post

from .cart import Carrinho
from .forms import CheckoutForm
from .models import Categoria, ItemPedido, Pedido, Produto


def home(request):
    posts = Post.objects.filter(publicado=True)[:3]
    produtos = Produto.objects.filter(ativo=True)[:4]
    return render(
        request,
        "home.html",
        {"posts": posts, "produtos": produtos},
    )


def lista_produtos(request, slug_categoria=None):
    categoria = None
    produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.all()

    if slug_categoria:
        categoria = get_object_or_404(Categoria, slug=slug_categoria)
        produtos = produtos.filter(categoria=categoria)

    return render(
        request,
        "loja/lista.html",
        {
            "produtos": produtos,
            "categorias": categorias,
            "categoria_atual": categoria,
        },
    )


def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    return render(request, "loja/detalhe.html", {"produto": produto})


@require_POST
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    if not produto.disponivel:
        messages.error(request, "Produto sem estoque.")
        return redirect("loja:detalhe", slug=produto.slug)

    carrinho = Carrinho(request)
    quantidade = int(request.POST.get("quantidade", 1))
    carrinho.adicionar(produto, quantidade=max(1, quantidade))
    messages.success(request, f'"{produto.nome}" adicionado ao carrinho.')
    return redirect("loja:carrinho")


@require_POST
def remover_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = Carrinho(request)
    carrinho.remover(produto)
    messages.info(request, f'"{produto.nome}" removido do carrinho.')
    return redirect("loja:carrinho")


def ver_carrinho(request):
    carrinho = Carrinho(request)
    return render(request, "loja/carrinho.html", {"carrinho": carrinho})


def checkout(request):
    carrinho = Carrinho(request)
    if len(carrinho) == 0:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect("loja:lista")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedido = Pedido.objects.create(
                nome_cliente=form.cleaned_data["nome_cliente"],
                email=form.cleaned_data["email"],
                endereco=form.cleaned_data["endereco"],
            )
            for item in carrinho:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item["produto"],
                    preco=item["preco"],
                    quantidade=item["quantidade"],
                )
                produto = item["produto"]
                produto.estoque = max(0, produto.estoque - item["quantidade"])
                produto.save(update_fields=["estoque"])

            carrinho.limpar()
            messages.success(request, f"Pedido #{pedido.pk} criado com sucesso!")
            return redirect("loja:pedido_ok", pedido_id=pedido.pk)
    else:
        form = CheckoutForm()

    return render(
        request,
        "loja/checkout.html",
        {"form": form, "carrinho": carrinho},
    )


def pedido_ok(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, "loja/pedido_ok.html", {"pedido": pedido})
