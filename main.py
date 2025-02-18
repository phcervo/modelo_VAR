import price_funcs as pf
import options_func as of
import var_func as vf
import numpy as np
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define ativos da carteira
ativos = ['PETR3','VALE3','ITUB4']
# Define quantidades do ativo na carteira
qtd = [2000,2000,2000]

# Data de referência
data_inicial = '2024-06-01'
data_final = '2024-09-01'

# Separa os ativos da carteira entre ações e opções (de acordo com o ticker do ativo)
lista_ativos = []
lista_opcoes = []
qtd_acoes = []
qtd_opcoes = []
i = 0
for ativo in ativos:
    if of.isoption(ativo):
        lista_opcoes.append(ativo)
        qtd_opcoes.append(qtd[i])
        i += 1
    else:
        lista_ativos.append(ativo)
        qtd_acoes.append(qtd[i])
        i += 1

opt_tuple = tuple(zip(lista_opcoes,qtd_opcoes))
infos_opcoes = []
for opcao in opt_tuple:
    infos = of.infos_opt(opcao[0],2025)
    infos_opcoes.append(infos)
# Inicia lista de subjacentes dos ativos (opções e ações)
subjacentes = []
for infos in infos_opcoes:
    subjacente = infos[0]
    subjacentes.append(subjacente)

total_ativos = lista_ativos + subjacentes
# Busca as cotações dos ativos da carteira na API do Yahoo Finance
cotacoes = pf.get_cotacoes_yahoo(total_ativos,data_inicial,data_final)
try:
    cotacoes.shape[1]
except:
    ativo = total_ativos[0] + '.SA'
    cotacoes = cotacoes.reset_index()
    cotacoes.columns = ['Date',ativo]
    cotacoes = cotacoes.set_index('Date')
# Calcula o log retorno dos ativos
retornos = cotacoes.apply(pf.calcula_log_retorno)
# Calcula a matriz de covariância dos ativos
matriz_covar = vf.matriz_covar(retornos)

# Define data de cálculo do VaR
data_calculo = datetime(2025,2,10)
# Define Taxa de juros 
r = 0.1315
lista_delta = []

# Tratamento para os casos de opções
for opcoes in infos_opcoes:
    subjacente = opcoes[0] + '.SA'
    cotac_recente = cotacoes[subjacente].iloc[-1]
    retornos_ativo = retornos[subjacente]
    vol_ewma = vf.vol_ewma(retornos_ativo)
    vencimento = (opcoes[1] - data_calculo).days / 360
    strike_price = opcoes[2]
    opt_type = opcoes[3]
    delta = of.opt_delta(cotac_recente,strike_price,vencimento,r,vol_ewma,opt_type)
    lista_delta.append(delta)

final_opcoes = list(zip(subjacentes,qtd_opcoes,lista_delta))
subjacente_final = []
qtd_subjacente = []
for infos in final_opcoes:
    qtd_subjacente.append(infos[1] * infos[2]) 
    subjacente_final.append(infos[0])

ativos_final = lista_ativos + subjacente_final
qtd_final = qtd_acoes + qtd_subjacente

# Remover duplicados (pra caso de apenas 1 ativo)
if cotacoes.shape[1] == 1:
    ativos_final = list(set(ativos_final))

# Junta quantidades se mesmo ativo na carteira
if len(ativos_final)<=1:
    qtd_final = sum(qtd_final)
    qtd_final_lista = []
    qtd_final_lista.append(qtd_final)
    qtd_final = qtd_final_lista

# Calcula a posição em financeiro da carteira
notional = pf.notional_carteira(ativos_final,qtd_final,cotacoes)
# Define valor crítico para o cálculo do VaR Paramétrico (padrão 95%)
ic = vf.valor_critico(0.95)
# Calcula o VaR com os parâmetros passados
var = vf.calcula_var(ic,notional,matriz_covar)
notional_carteira = sum(notional)
# Printa o VaR calculado
print(f'O VaR da carteira é de R$ {var}.')
print(f'O VaR percentual é de {round((var/notional_carteira) * 100, 4)}%')
