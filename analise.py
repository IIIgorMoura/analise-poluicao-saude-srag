import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from streamlit_tags import st_tags
import numpy as np
 

# DataFrames

df_prop_23 = pd.read_excel('./DBs/df_srag_populacao_PRINCIPAIS_PRECISO_23.xlsx')
df_prop_24 = pd.read_excel('./DBs/df_srag_populacao_PRINCIPAIS_PRECISO_24.xlsx')


df_prop_23_sorted = df_prop_23.sort_values(by='PROPORCAO', ascending=False).reset_index(drop=True)
df_prop_23_sorted = df_prop_23_sorted.iloc[:19]
df_prop_24_sorted = df_prop_24.sort_values(by='PROPORCAO', ascending=False).reset_index(drop=True)
df_prop_24_sorted = df_prop_24_sorted.iloc[:20]

# Configurações  iniciais
st.set_page_config(page_title="Impacto - Indústria Química", page_icon="📈", layout="wide")
# st.sidebar.header("Selecione os Filtros")


def Home():
    st.title('🏭 Impacto das Indústrias Químicas na Saúde e Qualidade de Vida da População')

    total_srag = df_prop_23['QUANTIDADE DE CASOS'].sum() + df_prop_24['QUANTIDADE DE CASOS'].sum()
    obitos_srag = 8913 + 8009

    st.write(' ')
    st.write(' ')

    total1, total2, total3 = st.columns(3)
    with total1:
        st.metric('Total de Casos SRAG desde 2023 em SP', value=int(total_srag))
    with total2:
        st.metric('Total de Óbitos por SRAG desde 2023 em SP', value=int(obitos_srag))
    with total3:
        st.metric('Principal Poluente Responsável', value=str('MP2.5'))


    
    st.markdown('- - -')

    # st.sidebar.write('filtro: POLUENTE')
    # st.sidebar.write('filtro: PERÍODO')

    # GRÁFICO: Poluição MÉDIA por REGIÃO
    poluentes = ['BS-MP10', 'BS-MP2.5', 'BS-NO2', 'BS-SO2',
             'AT-MP10', 'AT-MP2.5', 'AT-NO2', 'AT-SO2']

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio',
            'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
            'Novembro', 'Dezembro']

    cidades_interesse = [
        'Santos - Ponta da Praia',
        'Cubatão - Vale do Mogi',
        'Cubatão - V. Parisi',
        'Guarulhos - Pimentas',
        'Osasco',
        'Congonhas',
        'Cerqueira César',
        'Marg. Tietê - Ponte'
    ]

    media_poluentes = pd.DataFrame(index=cidades_interesse, columns=poluentes)

    # Calcular médias
    for poluente in poluentes:
        df_poluicao_regiao = pd.read_excel('./DBs/df_poluicao_regiao_filtrado.xlsx', sheet_name=poluente)
        df_filtrado = df_poluicao_regiao[df_poluicao_regiao['Local de Amostragem'].isin(cidades_interesse)]
        
        for cidade in cidades_interesse:
            df_cidade = df_filtrado[df_filtrado['Local de Amostragem'] == cidade]
            media = df_cidade[meses].mean().mean() if not df_cidade.empty else np.nan
            media_poluentes.loc[cidade, poluente] = media

    media_poluentes = media_poluentes.astype(float)

    # Cores por tipo
    cores_tipos = {
        'MP10': '#1f77b4',   # Azul médio → partículas maiores
        'MP2.5': '#aec7e8',  # Azul claro → partículas menores
        'NO2':  '#ff7f0e',   # Laranja → gases tóxicos, chama atenção
        'SO2':  '#d62728'    # Vermelho → ácido sulfuroso, mais nocivo
    }

    # Gráfico com Plotly
    fig_poluicao_regiao = go.Figure()
    x = np.arange(len(cidades_interesse))
    largura = 0.1

    for i, poluente in enumerate(poluentes):
        tipo = poluente.split('-')[1]
        cor = cores_tipos.get(tipo, '#000000')
        fig_poluicao_regiao.add_trace(go.Bar(
            x=[cidade for cidade in cidades_interesse],
            y=media_poluentes[poluente],
            name=poluente,
            marker_color=cor,
            offsetgroup=i,
        ))

    # Layout
    fig_poluicao_regiao.update_layout(
        title='📊 Média Anual dos Poluentes por Cidade',
        xaxis_title='Cidade',
        yaxis_title='Média Anual do Nível de Poluição',
        barmode='group',
        xaxis_tickangle=-45,
        template='plotly_white',
        legend_title='Poluentes',
        height=600
    )

    # Exibir no Streamlit
    st.plotly_chart(fig_poluicao_regiao, use_container_width=True)






    # GRÁFICO: Poluente no período por Cidade
    cidades_interesse = [
        'Cubatão - Centro',
        'Cubatão - Vale do Mogi',
        'Cubatão - V. Parisi',
        'Osasco',
        'Congonhas',
        'Marg. Tietê - Ponte',
        'Itaquera',
        'Santo Amaro'
    ]

    # Definir meses
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio',
            'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
            'Novembro', 'Dezembro']


        # Função para ler e filtrar os dados de cada poluente
    def ler_dados_poluente(poluente, regioes):
        # Ler os dados do poluente para as regiões
        df_baixada_santista = pd.read_excel('./DBs/df_poluicao_regiao_filtrado.xlsx', sheet_name=f'BS-{poluente}')
        df_alto_tiete = pd.read_excel('./DBs/df_poluicao_regiao_filtrado.xlsx', sheet_name=f'AT-{poluente}')
        
        # Concatenar ambos os dataframes
        df_total = pd.concat([df_baixada_santista, df_alto_tiete])
        
        # Filtrar pelas cidades de interesse
        df_filtrado = df_total[df_total['Local de Amostragem'].isin(cidades_interesse)]
        
        return df_filtrado

    # Ler os dados de MP10 e SO2
    df_mp10 = ler_dados_poluente('MP10', ['BS', 'AT'])
    df_mp2 = ler_dados_poluente('MP2.5', ['BS', 'AT'])

    # Configurar cores para as cidades
    cores_cidades = ["#3355FF", "#FF3388", "#A033FF", '#33FF92', "#EBFF33", "#FF5733", "#6A5ACD", "#FF8C00"]

    # Função para adicionar as linhas de cada cidade ao gráfico
    def adicionar_linhas(df_poluente, nome_poluente, cor, fig):
        for i, cidade in enumerate(cidades_interesse):
            df_cidade = df_poluente[df_poluente['Local de Amostragem'] == cidade]
            
            if not df_cidade.empty:
                valores = df_cidade[meses].values.flatten()
                
                # Adicionar a linha correspondente a cada cidade
                fig.add_trace(go.Scatter(
                    x=meses,
                    y=valores,
                    mode='lines+markers',
                    name=f"{cidade} - {nome_poluente}",
                    line=dict(color=cor[i], width=2),
                    marker=dict(size=6)
                ))

    # Criar o gráfico para MP10
    fig_mp10 = go.Figure()
    adicionar_linhas(df_mp10, 'MP10', cores_cidades, fig_mp10)
    fig_mp10.update_layout(
        title='📊 Evolução do Poluente MP10 nas Cidades ao Longo de 2024',
        xaxis_title='Meses',
        yaxis_title='Nível de Poluição (MP10)',
        xaxis=dict(tickmode='array', tickvals=meses, tickangle=-60),
        template='plotly_white',
        legend_title="Cidades",
        height=600
    )

    # Criar o gráfico para SO2
    fig_so2 = go.Figure()
    adicionar_linhas(df_mp2, 'MP2.5', cores_cidades, fig_so2)
    fig_so2.update_layout(
        title='📊 Evolução do Poluente MP2.5 nas Cidades ao Longo de 2024',
        xaxis_title='Meses',
        yaxis_title='Nível de Poluição (MP2.5)',
        xaxis=dict(tickmode='array', tickvals=meses, tickangle=-60),
        template='plotly_white',
        legend_title="Cidades",
        height=600
    )

    # Exibir os gráficos no Streamlit
    st.plotly_chart(fig_mp10, use_container_width=True)
    st.plotly_chart(fig_so2, use_container_width=True)










    # GRÁFICO: Proporção de Casos SRAG por 100.000 habitantes

    df_23 = df_prop_23_sorted.copy()
    df_23['Ano'] = '2023'

    df_24 = df_prop_24_sorted.copy()
    df_24['Ano'] = '2024'

    df_long = pd.concat([df_23, df_24], ignore_index=True)

    # Renomear coluna para padrão usado no gráfico
    df_long.rename(columns={'PROPORCAO': 'Proporcao por 100 mil'}, inplace=True)

    # Criar o gráfico interativo
    fig_prop_anos = px.bar(
        df_long,
        x='CIDADE',
        y='Proporcao por 100 mil',
        color='Ano',
        barmode='group',
        title='🏥 Casos de SRAG por cidade a cada 100.000 habitantes'
    )

    fig_prop_anos.update_layout(
        xaxis_title='Cidade',
        yaxis_title='Casos por 100 mil habitantes',
        legend_title='Ano',
        xaxis_tickangle=-60
    )

    # Exibir no Streamlit
    st.plotly_chart(fig_prop_anos, use_container_width=True)










    # GRÁFICO: Previsão de casos SRAG até 2026
# Coloque todo o processo de treino e plotagem dentro do spinner
    with st.spinner('⏳ Estimando incidência de SRAG nos próximos anos usando séries temporais...'):
        df_23= pd.read_csv('./DBs/SRAG_23_filtrar.csv', encoding='latin1', sep=';')
        df_24 = pd.read_csv('./DBs/SRAG_24_filtrar.csv', encoding='latin1', sep=';')

        def preprocess(df, ano_max):
            df = df.dropna(subset=['DATA DE ENTRADA'])
            df['DATA DE ENTRADA'] = pd.to_datetime(df['DATA DE ENTRADA'], format='%d/%m/%Y', errors='coerce')
            df = df[df['ESTADO'] == 'SP']
            df = df[df['DATA DE ENTRADA'].dt.year <= ano_max]
            return df

        df_24_alt = preprocess(df_24, 2024)
        df_23_alt = preprocess(df_23, 2023)

        # === AGRUPAMENTO SEMANAL ===
        df_model = pd.concat([df_23_alt[['DATA DE ENTRADA']], df_24_alt[['DATA DE ENTRADA']]])
        df_model = df_model.groupby('DATA DE ENTRADA').size()
        df_model_weekly = df_model.resample('W').sum().reset_index(name='CASOS')
        df_model_weekly.set_index('DATA DE ENTRADA', inplace=True)
        df_model_weekly = df_model_weekly.fillna(0)

        # === TREINO E PREVISÃO ===
        train = df_model_weekly[df_model_weekly.index.year <= 2024]
        model = ARIMA(train['CASOS'], order=(48, 0, 3))  # Parâmetros podem ser ajustados
        model_fit = model.fit()

        # Prever 52 semanas de 2025
        steps = 104
        future_dates = pd.date_range(start='2025-01-01', periods=steps, freq='W-SUN')
        previsaoArima = model_fit.forecast(steps=steps)
        df_previsoes = pd.DataFrame({'ds': future_dates, 'Previsao_ARIMA': previsaoArima})

        # === GRÁFICO INTERATIVO COM PLOTLY ===
        fig_previsao = go.Figure()

        # Histórico 2023-2024
        fig_previsao.add_trace(go.Scatter(
            x=df_model_weekly.index,
            y=df_model_weekly['CASOS'],
            mode='lines',
            name='Histórico (2023-2024)',
            line=dict(color='red')
        ))

        # Previsão 2025
        fig_previsao.add_trace(go.Scatter(
            x=df_previsoes['ds'],
            y=df_previsoes['Previsao_ARIMA'],
            mode='lines',
            name='Previsão ARIMA (2025-2026)',
            line=dict(color='green', dash='dash')
        ))

        fig_previsao.update_layout(
            title='📉 Casos Semanais de SRAG em SP - Previsão com Machine Learning',
            xaxis_title='Período',
            yaxis_title='Número de Casos',
            hovermode='x unified',
            template='plotly_white',
            xaxis_tickformat='%b\n%Y',
    
        )

        st.plotly_chart(fig_previsao, use_container_width=True)



Home()