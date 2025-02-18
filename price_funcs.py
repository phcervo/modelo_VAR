import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
import yfinance
from scipy.stats import norm

yfinance.pdr_override()

def get_cotacoes_yahoo(ativos, data_inicial,data_final):
    lista_nova = []
    for ativo in ativos:
        ativo = ativo + '.SA'
        lista_nova.append(ativo)
    cotacoes = pdr.get_data_yahoo(lista_nova,data_inicial,data_final)['Adj Close']
    return cotacoes

def calcula_log_retorno(precos):
    log_retorno = np.log(np.array(precos[1:])/np.array(precos[:-1]))
    return log_retorno


def notional_carteira(ativos,qtd,cotacoes):
    carteira = list(zip(ativos,qtd))
    carteira.sort()
    i = 0
    notional = 0
    lista_notional = []
    cotacoes_recente = cotacoes.iloc[-1,:]
    for ativo in carteira:
        notional = ativo[1] * cotacoes_recente.iloc[i]
        lista_notional.append(notional)
        i += 1
    return lista_notional