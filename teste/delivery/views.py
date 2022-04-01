from curses.ascii import isdigit
from .models import Loja, Motoboy, Pedido
from django.http import HttpResponse, HttpResponseBadRequest
from itertools import cycle, islice
import json


def distribuicao():

    lojas = Loja.objects.all()
    motoboys = Motoboy.objects.all()
    pedidos = Pedido.objects.all()


    lista_motoboys = []
    for motoboy in motoboys:
        lista_motoboys.append(str(motoboy))

    lista_lojas = []
    for loja in lojas:
        lista_lojas.append(str(loja))

    query_prioridade = Motoboy.objects.exclude(prioridade_loja__isnull=True)
    
    lista_prioridades = []
    prioridades = {}

    for motoboy in query_prioridade:
        prioridades = {
            'motoboy': motoboy,
            'loja': str(motoboy.prioridade_loja)
        }
        lista_prioridades.append(prioridades)

    prioridades_motoboy = [str(x['motoboy']) for x in lista_prioridades]
    prioridades_loja = [str(x['loja']) for x in lista_prioridades]

    qtde_motoboys_sem_prioridade = len(lista_motoboys) - len(prioridades_motoboy)

    for item in prioridades_motoboy:
        lista_motoboys_reordenada = lista_motoboys.copy()
        lista_motoboys_reordenada.remove(str(item))
        lista_motoboys_reordenada.insert(0, str(item))

    quantidade_pedidos = len(pedidos)
    lista_motoboys_expandida = list(islice(cycle(lista_motoboys_reordenada), quantidade_pedidos))

    ordem_pedidos_original = []
    for pedido in pedidos:
        ordem_pedidos_original.append(str(pedido.loja))

    for prioridade in prioridades_loja:
        lista_lojas_sem_prioridade = lista_lojas.copy()
        lista_lojas_sem_prioridade.remove(prioridade)

        pedidos_sem_prioridade = ordem_pedidos_original.copy()
        pedidos_sem_prioridade = [item for item in pedidos_sem_prioridade if item != prioridade]

        pedidos_com_prioridade = ordem_pedidos_original.copy()
        pedidos_com_prioridade = [item for item in pedidos_com_prioridade if item == prioridade]

    ordem_pedidos_nova = []
    for pedido in range(quantidade_pedidos):
        if len(pedidos_com_prioridade) > 0:
            valor = pedidos_com_prioridade.pop(0)
            ordem_pedidos_nova.append(valor)

        push_motoboys_sem_prioridade = qtde_motoboys_sem_prioridade
        while (len(pedidos_sem_prioridade) > 0 and push_motoboys_sem_prioridade > 0):
            valor = pedidos_sem_prioridade.pop(0)
            ordem_pedidos_nova.append(valor)
            push_motoboys_sem_prioridade -= 1

    ordem_pedidos_nova_reordenada = [m for _, m in sorted(zip(ordem_pedidos_nova, lista_motoboys_expandida))]

    for index, pedido in enumerate(pedidos):
        m = Motoboy.objects.filter(id=ordem_pedidos_nova_reordenada[index])[0]
        pedido.motoboy = m
        pedido.save()

    distribuicao = []

    for motoboy in lista_motoboys:

        obj = {}
        obj['motoboy_id'] = int(motoboy)
        obj['pedidos'] = []

        pedidos_motoboy = list(Pedido.objects.filter(motoboy=motoboy))
        valor_total = 0

        for pedido in pedidos_motoboy:
            obj['pedidos'].append(
                {
                    'id': pedido.id,
                    'loja': pedido.loja.id
                }
            )

            loja_pedido = list(Loja.objects.filter(id=pedido.loja.id))[0]
            motoboy_pedido = list(Motoboy.objects.filter(id=pedido.motoboy.id))[0]
            valor_fixo = motoboy_pedido.valor_fixo
            comissao = loja_pedido.comissao
            valor_pedido = pedido.valor
            comissao_motoboy = comissao * valor_pedido

            valor_total = valor_total + valor_fixo + comissao_motoboy

        obj['total_recebido'] = valor_total

        distribuicao.append(obj)

    return distribuicao


def home(request):
    total_pedidos = distribuicao()
    return HttpResponse(json.dumps(total_pedidos))


def motoboy(request, pk):
    
    if len(Pedido.objects.filter(motoboy=pk)) == 0:
        message = {
            "message": "motoboy not found"
        }
        return HttpResponse(json.dumps(message))

    pedidos_pk = Pedido.objects.filter(motoboy=pk)

    motoboy_info = {}
    motoboy_info['motoboy_id'] = pk
    motoboy_info['pedidos'] = []

    valor_total = 0

    for pedido in pedidos_pk:
        motoboy_info['pedidos'].append(
            {
                'id': pedido.id,
                'loja': pedido.loja.id
            }
        )

        loja_pedido = list(Loja.objects.filter(id=pedido.loja.id))[0]
        motoboy_pedido = list(Motoboy.objects.filter(id=pedido.motoboy.id))[0]
        valor_fixo = motoboy_pedido.valor_fixo
        comissao = loja_pedido.comissao
        valor_pedido = pedido.valor
        comissao_motoboy = comissao * valor_pedido

        valor_total = valor_total + valor_fixo + comissao_motoboy

    motoboy_info['total_recebido'] = valor_total

    return HttpResponse(json.dumps(motoboy_info))
