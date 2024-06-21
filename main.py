import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório base ao sys.path
sys.path.append(str(Path(__file__).parent))

from modulos import risco, simulador_portifolio, fundamental_analysis

# Título do Dashboard
st.title('Dashboard do Mercado Financeiro')

# Barra de Navegação
page = st.sidebar.selectbox('Selecione a Página', ['Análise de Risco', 'Simulação de Portfólio', 'Análise Fundamentalista'])

# Navegação
if page == 'Análise de Risco':
    risco.show()
elif page == 'Simulação de Portfólio':
    simulador_portifolio.show()
elif page == 'Análise Fundamentalista':
    fundamental_analysis.show()
