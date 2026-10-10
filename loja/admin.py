from django.contrib import admin

from .models import Categoria, ItemPedido, Pedido, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "estoque", "ativo")
    list_filter = ("ativo", "categoria")
    search_fields = ("nome", "descricao")
    prepopulated_fields = {"slug": ("nome",)}
    list_editable = ("preco", "estoque", "ativo")


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("produto", "preco", "quantidade")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_cliente", "email", "status", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("nome_cliente", "email")
    inlines = [ItemPedidoInline]
