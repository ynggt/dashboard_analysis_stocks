import streamlit as st
import yfinance as yf
import sys
from pathlib import Path

# Adiciona o diretório base ao sys.path
sys.path.append(str(Path(__file__).parents[1]))

def show():
    st.header('Análise Fundamentalista')

    ticker = st.text_input('Digite o ticker da ação', 'AAPL')

    if ticker:
        stock = yf.Ticker(ticker)
        info = stock.info

        if info:
            st.write(info)
        else:
            st.error("Não foram encontrados dados fundamentalistas para o ticker fornecido.")
