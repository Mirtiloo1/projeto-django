from django.contrib import admin
from .models import Usuario, Categoria, Produto, Venda

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome","email")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "estoque", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nome", "descricao")

class VendaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "produto", "preco_da_venda", "data_da_compra")
    list_filter = ("data_da_compra", "cliente", "produto")
    search_fields = ("cliente__nome", "produto__nome")
    readonly_fields = ("data_da_compra",)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)