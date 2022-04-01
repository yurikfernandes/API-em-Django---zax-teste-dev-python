from django.db import models


class Loja(models.Model):

    comissao = models.FloatField()

    def __str__(self):
        return str(self.id)


class Motoboy(models.Model):

    valor_fixo = models.FloatField()
    prioridade_loja = models.ForeignKey(
        Loja, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)


class Pedido(models.Model):

    valor = models.FloatField(null=False)
    loja = models.ForeignKey(Loja, null=False, on_delete=models.CASCADE)
    motoboy = models.ForeignKey(
        Motoboy, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
