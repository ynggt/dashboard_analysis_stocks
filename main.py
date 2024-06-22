import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório base ao sys.path
sys.path.append(str(Path(__file__).parent))

from modulos import analise_fundamentalista, risco, simulacao_carteira

# Título do Dashboard


# Barra de Navegação
st.sidebar.image("imagens/logotipo.png")
page = st.sidebar.selectbox('Selecione a Página', ['Análise de Risco', 'Fronteira Eficiente', 'Análise Fundamentalista','Simulação de Carteira'])


# Navegação
if page == 'Análise de Risco':
    risco.show()
elif page == 'Fronteira Eficiente':
    fronteira_eficiente.show()
elif page == 'Análise Fundamentalista':
    analise_fundamentalista.show()
elif page == 'Simulação de Carteira':
    simulacao_carteira.show()