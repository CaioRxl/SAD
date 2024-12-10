import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do layout do Streamlit
st.set_page_config(page_title="Análise de Desmatamento - PRODES", layout="wide")

# Título do aplicativo
st.title("Análise do Desmatamento na Amazônia Legal")
st.subheader("Dados disponibilizados pelo PRODES")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Carregue o arquivo desejado", type="csv")

if uploaded_file:
    # Carregar os dados
    df = pd.read_csv(uploaded_file)

    # Conversão da coluna 'referencia' para formato datetime
    df['referencia'] = pd.to_datetime(df['referencia'], format='%Y')

    # Criar seleções de filtros
    st.sidebar.header("Filtros")
    start_year = st.sidebar.slider("Selecione o ano Inicial", int(df['referencia'].dt.year.min()), int(df['referencia'].dt.year.max()), int(df['referencia'].dt.year.min()))
    end_year = st.sidebar.slider("Selecione o ano Final", int(df['referencia'].dt.year.min()), int(df['referencia'].dt.year.max()), int(df['referencia'].dt.year.max()))

    filtered_df = df[(df['referencia'].dt.year >= start_year) & (df['referencia'].dt.year <= end_year)]

    # Início das Visualizações
    st.subheader("Análises Gráficas")

    # Evolução do desmatamento total por ano
    fig_total = px.area(
    filtered_df, x='referencia', y='area_total_desmatamento', 
    title='Evolução do Desmatamento Total', 
    labels={"referencia": "Ano", "area_total_desmatamento": "Área Total Desmatada (km²)"}
    )
    st.plotly_chart(fig_total, use_container_width=True)


    # Desmatamento por estado
    estados = ['acre', 'amazonas', 'amapa', 'maranhao', 'mato_grosso', 'para', 'rondonia', 'roraima', 'tocantins']
    total_por_estado = filtered_df[estados].sum().reset_index()
    total_por_estado.columns = ['estado', 'desmatamento']
    total_por_estado = total_por_estado.sort_values(by='desmatamento', ascending=True)
    fig_states = px.bar(
        total_por_estado, x='desmatamento', y='estado', orientation='h', 
        title='Desmatamento Total por Estado', 
        labels={"desmatamento": "Área Desmatada (km²)", "estado": "Estado"},
        text='desmatamento'
    )
    fig_states.update_traces(textposition="outside")
    st.plotly_chart(fig_states, use_container_width=True)

    # Gráfico de dispersão: Desmatamento total vs. Ano
    fig_scatter = px.scatter(
        filtered_df, x='referencia', y='area_total_desmatamento', 
        title='Dispersão: Desmatamento Total vs. Ano', 
        labels={"referencia": "Ano", "area_total_desmatamento": "Área Total Desmatada (km²)"},
        size='area_total_desmatamento', color='area_total_desmatamento',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico de barras empilhadas: Contribuição de cada estado no desmatamento ao longo dos anos
    fig_stacked = px.bar(
        filtered_df, x='referencia', y=estados, 
        title='Contribuição dos Estados no Desmatamento ao Longo dos Anos', 
        labels={"referencia": "Ano", "value": "Área Desmatada (km²)"},
        barmode='stack'
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    # Tabela com os dados
    st.subheader("Visão Geral")
    st.dataframe(filtered_df)

else:
    st.info("Por favor, carregue o arquivo para iniciar a análise.")