import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime

def bsm_metodo(S, K, T, r, vol, opt_type):
    """
    S: Preço atual do ativo subjacente
    K: Preço de exercício
    T: Tempo até o vencimento (em anos)
    r: Taxa de juros livre de risco (continua)
    vol: Volatilidade do ativo subjacente
    opt_type: 'c' ou 'p' para definir o tipo de opção (call ou put)
    """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    if opt_type == 'c':
        preco = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return preco
    elif opt_type == 'p':
        preco = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return preco
    else:
        print("Tipo de opção incorreto.")

# Calcula delta da opção
def opt_delta(S, K, T, r, vol, opt_type):
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    if opt_type == 'c':
        delta = norm.cdf(d1)
        return delta
    elif opt_type == 'p':
        delta = norm.cdf(d1) - 1
        return delta
    else:
        print("Tipo de opção incorreto.")

def isoption(ativo):
    if len(ativo)>6:
        return True


def infos_opt(ativo,ano_venc):
    """
    Idealmente, as informações devem ser consultadas em 'https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/posicoes-em-aberto/'
    ou outra fonte de dados. Os dados abaixo funcionarão como uma aproximação.
    Ano de vencimento da opção deve ser imputado
    """
    subjacente = ativo[:4] + '3'
    exercicio = float(ativo[5:])
    vencimento = ativo[4]
    lista_call = ['A','B','C','D','E','F','G','H','I','J','K','L']
    lista_put = ['M','N','O','P','Q','R','S','T','U','V','W','X']
    dict_call = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12}
    dict_put = {'M':1,'N':2,'O':3,'P':4,'Q':5,'R':6,'S':7,'T':8,'U':9,'V':10,'W':11,'X':12}

    if vencimento in lista_call:
        opt_type = 'c'
        mes_venc = dict_call.get(vencimento)
    else:
        opt_type = 'p'
        mes_venc = dict_put.get(vencimento)

    vencimento = datetime(ano_venc,mes_venc,16)

    return [subjacente,vencimento,exercicio,opt_type]