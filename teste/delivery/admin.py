from django.contrib import admin

from .models import Loja, Motoboy, Pedido

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ['id', 'comissao']

@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor_fixo', 'prioridade_loja']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor', 'loja', 'motoboy']
