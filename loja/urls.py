from django.urls import path

from . import views

app_name = "loja"

urlpatterns = [
    path("", views.lista_produtos, name="lista"),
    path("categoria/<slug:slug_categoria>/", views.lista_produtos, name="lista_categoria"),
    path("produto/<slug:slug>/", views.detalhe_produto, name="detalhe"),
    path("carrinho/", views.ver_carrinho, name="carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar"),
    path("carrinho/remover/<int:produto_id>/", views.remover_do_carrinho, name="remover"),
    path("checkout/", views.checkout, name="checkout"),
    path("pedido/<int:pedido_id>/", views.pedido_ok, name="pedido_ok"),
]
