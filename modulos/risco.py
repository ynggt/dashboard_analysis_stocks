import streamlit as st
import datetime as dt
import sys
from pathlib import Path

# Adiciona o diretório base ao sys.path
#sys.path.append(str(Path(__file__).parents[1]))

from utils.calculations import var_historico, var_parametrico

def show():
    st.header("Calculadora VaR de Ações")

    # Entradas do usuário
    ativo = st.text_input("Ativo:")
    data_inicial = st.date_input("Data Inicial", dt.date(2020, 1, 1))
    data_final = st.date_input("Data Final", dt.date.today())
    investimento = st.number_input("Valor do Investimento:", min_value=0)
    nivel_confianca = st.number_input("Nível de Confiança (0-1):", min_value=0.0, max_value=1.0, value=0.95)

    if st.button("Calcular VaR"):
        try:
            var_hist = var_historico(ativo, data_inicial, data_final, investimento, nivel_confianca)
            var_param = var_parametrico(ativo, data_inicial, data_final, investimento, nivel_confianca)
            
            st.write(f"VaR Histórico: R${var_hist:.2f}")
            st.write(f"VaR Paramétrico: R${var_param:.2f}")
        except ValueError as e:
            st.error(f"Erro: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
