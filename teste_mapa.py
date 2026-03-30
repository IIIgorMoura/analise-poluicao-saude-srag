# import streamlit as st
# import geopandas as gpd
# import folium
# from streamlit_folium import st_folium
# import branca.colormap as cm
# import pandas as pd
# import numpy as np
# import unidecode

# # Carrega o GeoDataFrame dos municípios de SP
# gdf = gpd.read_file("./SP_Municipios_2024/SP_Municipios_2024.shp")

# # Carrega seu DataFrame com as métricas
# df = pd.read_excel('./DBs/df_srag_populacao_PRINCIPAIS_PRECISO_23.xlsx')

# # Padroniza nomes para unir
# gdf['NOME_MUNIC'] = gdf['NM_MUN'].str.upper()
# df['CIDADE'] = df['CIDADE'].str.upper()

# # Merge no GeoDataFrame
# gdf = gdf.merge(df, left_on='NOME_MUNIC', right_on='CIDADE', how='left')

# def normalize_name(name):
#     if pd.isna(name):
#         return ''
#     return unidecode.unidecode(name).upper().strip()

# # Normaliza
# gdf['NOME_MUNIC'] = gdf['NM_MUN'].apply(normalize_name)
# df['CIDADE'] = df['CIDADE'].apply(normalize_name)

# # Filtra
# gdf_filtrado = gdf[gdf['NOME_MUNIC'].isin(df['CIDADE'])]

# # Agora faz o merge só com essas cidades
# gdf_filtrado = gdf_filtrado.merge(df, left_on='NOME_MUNIC', right_on='CIDADE', how='left')

# # Função para normalizar strings: sem acento e maiúscula
# def normalize_name(name):
#     if pd.isna(name):
#         return ''
#     return unidecode.unidecode(name).upper().strip()

# # Aplica no GeoDataFrame
# gdf['NOME_MUNIC'] = gdf['NM_MUN'].apply(normalize_name)

# # Aplica no DataFrame do DB
# df['CIDADE'] = df['CIDADE'].apply(normalize_name)

# # Cidades no gdf que NÃO estão no df
# # cidades_sem_dados = set(gdf['NOME_MUNIC']) - set(df['CIDADE'])
# # print("Cidades do gdf sem dados no df:", cidades_sem_dados)

# # # Cidades no df que NÃO estão no gdf
# # cidades_fora_gdf = set(df['CIDADE']) - set(gdf['NOME_MUNIC'])
# # print("Cidades do df não encontradas no gdf:", cidades_fora_gdf)

# # Ajusta mínimo e máximo para PROPORCAO
# min_val, max_val = 0, 1100  # como você mencionou, até cerca de 1080

# # Colormap cinza claro até vermelho forte
# colormap = cm.LinearColormap(colors=['#f0f0f0', '#ff4d4d'], vmin=min_val, vmax=max_val)

# # Função de estilo usando PROPORCAO
# def style_function(feature):
#     val = feature['properties']['PROPORCAO']
#     if val is None or np.isnan(val) or val == 0:
#         return {'fillColor': '#cccccc', 'color': 'black', 'weight': 1.2, 'fillOpacity': 0.3}
#     else:
#         return {'fillColor': colormap(val), 'color': 'black', 'weight': 1.2, 'fillOpacity': 0.7}

# # Cria mapa centralizado
# m = folium.Map(location=[-23.55, -46.63], zoom_start=8, tiles='cartodbpositron')

# # Tooltip mostrando o nome e o valor de PROPORCAO
# tooltip = folium.GeoJsonTooltip(
#     fields=['NOME_MUNIC', 'PROPORCAO'],
#     aliases=['Cidade:', 'Proporção (casos por 100k):'],
#     localize=True,
#     labels=True,
#     sticky=False
# )

# # Adiciona polígonos no mapa com estilos e tooltip
# folium.GeoJson(
#     gdf.to_json(),
#     style_function=style_function,
#     tooltip=tooltip
# ).add_to(m)

# # Legenda com título adequado
# colormap.caption = 'Proporção de Casos SRAG por 100.000 habitantes'
# colormap.add_to(m)

# # Mostra no Streamlit
# st_folium(m, width=700, height=500)