from django.db import models
from .Base.models import BaseModel, QuerySet


class Ativos(BaseModel):
    class classe(models.TextChoices):
        Acoes = 'Ações', ('Ações_BR')
        FIIs = 'FIIs', ('Fundos Imobiliários')
        Stocks = 'Stocks', ('Stocks')
        REITs = 'REITs', ('Reits americanos')
        cryptos = 'cryptos', ('Criptoativos')
        ETF_BR = 'ETF-BR', ('ETF BR')
        ETF_US = 'ETF-US', ('ETF US')
        Caixa = 'Caixa', ('Caixa')

    classe = models.CharField(max_length=10, choices=classe.choices, default=classe.Caixa)
    nome = models.CharField(max_length=10)
    quantidade = models.IntegerField(null=True, blank=True)
    saldo = models.FloatField(null=True, blank=True)
    pm = models.FloatField(null=True, blank=True)
    valor_atual = models.FloatField(null=True, blank=True)
    lucro_preju = models.FloatField(null=True, blank=True)
    pminpago = models.FloatField(null=True, blank=True)
    pmaxpago = models.FloatField(null=True, blank=True)
    percentual_classe = models.CharField(max_length=10, null=True, blank=True)
    percentual_lucro = models.CharField(max_length=10, null=True, blank=True)
    saldo_USD = models.FloatField(null=True, blank=True)
    pm_USD = models.FloatField(null=True, blank=True)
    valor_atual_USD = models.FloatField(null=True, blank=True)
    percentual_patrimonio = models.CharField(max_length=10, null=True, blank=True)

    objects = QuerySet.as_manager()

    ''' classe = ações, fiis, etc
        nome = nome do ativo
        pm = preço médio
        valor_atual = valor de um único ativo após o fechamento do último dia útil
        lucro_prejo = valor nominal em reais do lucro ou prejuízo
        pminpago = preço mínimo pago por ativo
        pmaxpago = preço máximo pago por ativo
        percentual_classe = % total com relação à classe
        percentual_lucro = lucro ou prejuízo percentual
        saldo_USD = saldo convertido pra USD
        pm_USD = preço médio em USD
        valor_atual_USD = valor de um único ativo em USD
        percentual_patrimonio = percentual com o total do patrimônio.'''


class Patrimonio(BaseModel):
    valor = models.FloatField(null=True, blank=True, default=0)
    valor_acoes = models.FloatField(null=True, blank=True, default=0)
    percentual_acoes = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_fiis = models.FloatField(null=True, blank=True, default=0)
    percentual_fiis = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_stocks = models.FloatField(null=True, blank=True, default=0)
    percentual_stocks = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_reits = models.FloatField(null=True, blank=True, default=0)
    percentual_reits = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_cryptos = models.FloatField(null=True, blank=True, default=0)
    percentual_cryptos = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_etf_br = models.FloatField(null=True, blank=True, default=0)
    percentual_etfs_br = models.CharField(max_length=10, null=True, blank=True, default='')
    valor_etfs_us = models.FloatField(null=True, blank=True, default=0)
    percentual_etfs_us = models.CharField(max_length=10, null=True, blank=True, default='')
    dividendos_reinvestidos = models.FloatField(null=True, blank=True)
    ''' Cria-se apenas uma vez. O resto será atualizar.'''


class Registro(BaseModel):
    ativo_utilizado = models.CharField(max_length=10)
    total_saida = models.IntegerField()
    ativo_comprado = models.CharField(max_length=10)
    total_entrada = models.IntegerField()
    valor_unit_saida = models.FloatField()
    valor_unit_entrada = models.FloatField()
    unid_comprada_USD = models.FloatField()
    unid_vendida_USD = models.FloatField()
    taxas = models.FloatField(null=True, blank=True, default=0)
    cambio_USD = models.FloatField(null=True, blank=True, default=0)
    PM_Ativo_Comprado = models.FloatField(null=True, blank=True, default=0)
    origem_dividendos = models.BooleanField(null=True, blank=True)
