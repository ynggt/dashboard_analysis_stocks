import streamlit as st
import yfinance as yf
import investpy
import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
from scipy.optimize import minimize
import plotly.graph_objs as go

def show():
    st.header("Simulação de Carteira de Ações")

    # Obter lista de todas as ações brasileiras
    stocks = investpy.stocks.get_stocks(country='brazil')
    all_tickers = stocks['symbol'].tolist()

    # Inputs no sidebar
    with st.sidebar:
        st.header("Parâmetros de Simulação")
        
        # Seleção de múltiplos tickers
        tickers = st.multiselect('Selecione os tickers das ações', all_tickers)
        tickers = [t + ".SA" for t in tickers]

        data_inicial = st.date_input("Data Inicial", value=dt.date(2020, 1, 1))
        data_final = st.date_input("Data Final", value=dt.date.today())
        
        num_portfolios = st.number_input("Número de Portfólios Simulados", min_value=1000, max_value=50000, value=10000)

    # Caso tenha selecionado alguma ação
    if tickers:
        precos = yf.download(tickers, start=data_inicial, end=data_final)["Adj Close"]

        if not precos.empty:
            
            # Cálculo dos retornos diários
            retornos_diarios = precos.pct_change().dropna()
            retornos_diarios_zscore = stats.zscore(retornos_diarios)
            # Mostrar os preços ajustados
            st.subheader("Preços Ajustados")
            st.line_chart(precos)

            # Simulação de Portfólio
            num_acoes = len(tickers)

            # Arrays para armazenar os resultados
            resultados = np.zeros((3, num_portfolios))
            pesos_portfolios = []

            for i in range(num_portfolios):
                # Pesos aleatórios
                pesos = np.random.random(num_acoes)
                pesos /= np.sum(pesos)
                pesos_portfolios.append(pesos)
                
                # Retorno esperado e volatilidade do portfólio
                retorno_portfolio = np.sum(retornos_diarios.mean() * pesos) * 252
                volatilidade_portfolio = np.sqrt(np.dot(pesos.T, np.dot(retornos_diarios.cov() * 252, pesos)))
                sharpe_ratio = retorno_portfolio / volatilidade_portfolio
                
                # Armazenar os resultados
                resultados[0, i] = retorno_portfolio
                resultados[1, i] = volatilidade_portfolio
                resultados[2, i] = sharpe_ratio

            # DataFrame dos resultados
            resultados_df = pd.DataFrame(resultados.T, columns=['Retorno Esperado', 'Volatilidade', 'Sharpe Ratio'])

            # Melhor portfólio (com base no Sharpe Ratio)
            max_sharpe_idx = resultados_df['Sharpe Ratio'].idxmax()
            melhor_portfolio = resultados_df.loc[max_sharpe_idx]
            melhor_pesos = pesos_portfolios[max_sharpe_idx]

            # Calcular a linha da fronteira eficiente
            max_retornos = np.linspace(resultados_df['Retorno Esperado'].min(), resultados_df['Retorno Esperado'].max(), 100)
            ef_volatilidades = []

            def portfolio_volatility(weights, returns, cov_matrix):
                return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

            for ret in max_retornos:
                constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                               {'type': 'eq', 'fun': lambda x: np.sum(retornos_diarios.mean() * x) * 252 - ret})
                bounds = tuple((0, 1) for _ in range(num_acoes))
                result = minimize(portfolio_volatility, [1./num_acoes]*num_acoes, args=(retornos_diarios, retornos_diarios.cov() * 252),
                                  method='SLSQP', bounds=bounds, constraints=constraints)
                ef_volatilidades.append(result.fun)

            # Container para o gráfico de dispersão
            grafico_container = st.container()
            with grafico_container:
                st.subheader("Gráfico de Dispersão")
                
                fig = go.Figure()

                # Adicionando pontos dos ativos
                fig.add_trace(go.Scatter(
                    x=resultados_df['Volatilidade'],
                    y=resultados_df['Retorno Esperado'],
                    mode='markers',
                    marker=dict(size=5, color='blue', opacity=0.7),
                    name='Portfólios Simulados'
                ))

                # Adicionando a fronteira eficiente
                fig.add_trace(go.Scatter(
                    x=ef_volatilidades,
                    y=max_retornos,
                    mode='lines',
                    line=dict(color='green', width=2),
                    name='Fronteira Eficiente'
                ))

                # Destacando o ponto com o melhor índice de Sharpe
                fig.add_trace(go.Scatter(
                    x=[melhor_portfolio['Volatilidade']],
                    y=[melhor_portfolio['Retorno Esperado']],
                    mode='markers',
                    marker=dict(color='red', size=12, symbol='star'),
                    name='Melhor Índice de Sharpe'
                ))

                # Configurando layout do gráfico
                fig.update_layout(
                    title='Gráfico de Dispersão: Retorno Esperado vs Volatilidade',
                    xaxis_title='Volatilidade',
                    yaxis_title='Retorno Esperado',
                    showlegend=True
                )

                ## Adicionando o gráfico ao Streamlit
                st.plotly_chart(fig)

            # Container para as informações do melhor portfólio
            info_container = st.container()
            with info_container:
                st.subheader("Melhor Portfólio")
                st.write("Pesos:")
                for i, peso in enumerate(melhor_pesos):
                    st.write(f"{tickers[i]}: {peso:.2%}")

        else:
            st.write("Não foram encontrados dados para os tickers selecionados no período especificado.")

if __name__ == "__main__":
    show()
