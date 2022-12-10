import datetime
import requests
from time import sleep
from django.db.models import Sum
from ativos.models import Patrimonio, Ativos


# ALPHAVANTAGE
def quotation(nome):
    # api_key = "8QU6ELEHQEM8383U"
    # api_key2 = "J4ZSRVVHMVS5PEAR"
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={nome}&interval=1min&apikey={api_key}&outputsize=compact'
    # r = requests.get(url)
    # last_busday = r.json()['Meta Data']['3. Last Refreshed'][:10]
    # data = r.json()['Time Series (Daily)'][last_busday]['5. adjusted close']
    # float_data = float(data)
    # return round(float_data, 2)
    api_key = "8QU6ELEHQEM8383U"
    api_key2 = "J4ZSRVVHMVS5PEAR"
    # try:
    #     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={nome}&interval=1min&apikey={api_key}&outputsize=compact'
    #     r = requests.get(url)
    #     last_busday = r.json()['Meta Data']['3. Last Refreshed'][:10]
    #     data = r.json()['Time Series (Daily)'][last_busday]['5. adjusted close']
    #     float_data = float(data)
    #     return round(float_data, 2)
    # except:
    #     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={nome}&interval=1min&apikey={api_key2}&outputsize=compact'
    #     r = requests.get(url)
    #     last_busday = r.json()['Meta Data']['3. Last Refreshed'][:10]
    #     data = r.json()['Time Series (Daily)'][last_busday]['5. adjusted close']
    #     float_data = float(data)
    #     return round(float_data, 2)
    return 10

# USD = quotation('USDBRL')
USD = 5.25


def to_usd(valor):
    valor_usd = round(valor / USD, 2)
    return valor_usd


Atv = Ativos.objects.all()


def updated_full_patrimony_value(Atv):
    try:
        nomes = list(Atv.values_list('nome', flat=True).values())
        valor_total_ativo_tempo_real = []
        for n in nomes:
            quantidade = n['quantidade']
            cotacao = quotation(f"{n['nome']}.SAO") if n['classe'] in ['ações', 'fiis', 'etfs_br'] \
                else cotacao == quotation(f"{n['nome']}")
            valor_total_ativo_tempo_real.append(quantidade * cotacao)
        return sum(valor_total_ativo_tempo_real)
    except:
        return 0


def updated_full_acoes_value(Atv):
    try:
        nomes = list(Atv.filter(classe='ações').values())
        valor_acoes_tempo_real = []
        for n in nomes:
            quantidade = n['quantidade']
            cotacao = quotation(f"{n['nome']}.SAO")
            valor_acoes_tempo_real.append(quantidade * cotacao)
        return sum(valor_acoes_tempo_real)
    except:
        return 0


def updated_full_fiis_value(Atv):
    try:
        nomes = list(Atv.filter(classe='fiis').values())
        valor_fiis_tempo_real = []
        for n in nomes:
            quantidade = n['quantidade']
            cotacao = quotation(f"{n['nome']}.SAO")
            valor_fiis_tempo_real.append(quantidade * cotacao)
        return sum(valor_fiis_tempo_real)
    except:
        return 0


def validate_patrimonio():
    try:
        return Patrimonio.objects.get(id=1)
    except:
        return Patrimonio.objects.create(
            valor=0,
            valor_acoes=0,
            percentual_acoes='0"%"',
            valor_fiis=0,
            percentual_fiis='0"%"',
            valor_stocks=0,
            percentual_stocks='0"%"',
            valor_reits=0,
            percentual_reits='0"%"',
            valor_cryptos=0,
            percentual_cryptos='0"%"',
            valor_etf_br=0,
            percentual_etfs_br='0"%"',
            valor_etfs_us=0,
            percentual_etfs_us='0"%"',
            dividendos_reinvestidos=0
        )
