import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
import yfinance
from scipy.stats import norm

def matriz_covar(retornos,lambda_factor=0.94):
    n_ativos = retornos.shape[1]
    # Iniciar a matriz de variância e covariância EWMA
    variancia_ewma = np.var(retornos, axis=0)
    covar_ewma = retornos.cov().values

    # Calcula as volatilidades e covariâncias EWMA
    for t in range(1, len(retornos)):
        for i in range(n_ativos):
            variancia_ewma.iloc[i] = lambda_factor * variancia_ewma.iloc[i] + (1 - lambda_factor) * retornos.iloc[t-1, i]**2
            
            for j in range(i, n_ativos):
                covar_ewma[i, j] = lambda_factor * covar_ewma[i, j] + (1 - lambda_factor) * (retornos.iloc[t-1, i] * retornos.iloc[t-1, j])
                if i != j:  # Simetria da covariância
                    covar_ewma[j, i] = covar_ewma[i, j]

    # Constrói a matriz de covariância EWMA
    matriz_covar_ewma = np.zeros((n_ativos, n_ativos))
    for i in range(n_ativos):
        matriz_covar_ewma[i, i] = variancia_ewma.iloc[i]
        for j in range(i+1, n_ativos):
            matriz_covar_ewma[i, j] = covar_ewma[i, j]
            matriz_covar_ewma[j, i] = covar_ewma[i, j]
    
    return matriz_covar_ewma

def vol_ewma(retornos,lambda_factor=0.94):
    variancia_ewma = np.var(retornos, axis=0)
    for t in range(1, len(retornos)):
        variancia_ewma = lambda_factor * variancia_ewma + (1 - lambda_factor) * retornos.iloc[t-1]**2
        volat_ewma = np.sqrt(variancia_ewma) * (252**(1/2))
    return volat_ewma
 
def valor_critico(ic):
    valor_critico = norm.ppf(ic)
    return valor_critico

# Função matricial para o cálculo do VaR
def calcula_var(valor_critico, carteira, matriz_covariancia):
    carteira = np.array(carteira)
    var = valor_critico * np.sqrt(np.dot(carteira.T, np.dot(matriz_covariancia,carteira)))
    return var

