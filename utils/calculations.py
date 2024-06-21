import pandas as pd
from scipy.stats import norm
import numpy as np
import streamlit as st



################################## RISCO ##################################################
try:
    import yfinance as yf
except ImportError:
    print("Erro ao importar yfinance. Verifique sua instalação ou conexão com a internet.")

def var_historico(ativo, data_inicial, data_final, investimento, nivel_confianca):
    ativo_tratado = ativo.upper().replace(" ", "") + ".SA"
    dados = yf.download(ativo_tratado, start=data_inicial, end=data_final)

    precos = dados['Close']
    if precos.empty:
        raise ValueError(f"Não foram encontrados dados para o ativo {ativo_tratado} no período especificado.")

    retornos_logaritmicos = np.log(precos / precos.shift(1)).dropna()
    var_percentil = np.percentile(retornos_logaritmicos, (1 - nivel_confianca) * 100)
    var_hist = investimento * var_percentil
    return var_hist

def var_parametrico(ativo, data_inicial, data_final, investimento, nivel_confianca):
    ativo_tratado = ativo.upper().replace(" ", "") + ".SA"
    dados = yf.download(ativo_tratado, start=data_inicial, end=data_final)
    precos = dados['Close']
    if precos.empty:
        raise ValueError(f"Não foram encontrados dados para o ativo {ativo_tratado} no período especificado.")

    retornos_logaritmicos = [np.log(precos.iloc[i] / precos.iloc[i-1]) for i in range(1, len(precos))]
    vol_ativo = np.std(retornos_logaritmicos)
    var_param = investimento * norm.ppf(1 - nivel_confianca) * vol_ativo
    
    return var_param


# def var_montecarlo(atvio)


################################## RISCO /FIM ##################################################