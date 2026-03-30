# 🏭 Impacto da Poluição Industrial na Saúde Pública (SRAG)
**Análise de Correlação entre Polos Industriais e Síndrome Respiratória Aguda Grave**


## Visão Geral
Este projeto analisa a correlação estatística entre a proximidade de polos industriais no estado de São Paulo e a incidência de Síndrome Respiratória Aguda Grave (SRAG) entre 2023 e 2024. Utilizando técnicas de Ciência de Dados e Modelagem Preditiva, a análise identifica disparidades críticas na saúde pública e evidencia a inconsistência crítica de registros de monitoramento do poluentes em regiões de alto risco.

O objetivo é fornecer dados estruturados que facilitem a mensuração de indicadores ESG (Environmental, Social, and Governance), auxiliando na transparência sobre o impacto ambiental e na análise de riscos à saúde das comunidades situadas em zonas industriais.

---

## Principais Desafios: Data Hunting e ETL
* **Bases de Dados:** Busca, extração e tratamento de dados brutos de saúde pública para identificar casos de SRAG por município.
* **O Apagão do MP2.5:** Identificação crítica da ausência de registros sobre o **Material Particulado 2.5** (o mais nocivo à saúde) em polos críticos como Cubatão, evidenciando falhas no monitoramento ambiental. 
* **Acesso Restrito:** Recuperação de dados ambientais via bases de monitoramento com acesso controlado, superando a falta de transparência em portais de dados abertos.

---

## Insights Principais

### 1. O Custo do Ar (Top Incidências)
Cruzando o número de casos de SRAG por cidade proporcionalmente a cada 100.000 habitantes, identificamos o **Percentual Gravemente Impactado**. As cidades com maior atividade indústrias lideram o ranking de criticidade:

| Cidade (2023) | % Pop. Impactada | Perfil Regional |
| :--- | :--- | :--- |
| **São Caetano do Sul** | 1.08% | Alta densidade / Cinturão Industrial ABC |
| **Santos** | 0.50% | Influência Portuária e Logística Pesada |
| **Mauá** | 0.37% | Polo Petroquímico (RECAP) |
| **Paulínia** | 0.27% | Maior Polo Petroquímico da AL (REPLAN) |

<br>

Enquanto cidades que possuem perfis voltados à preservação ou turismo. Possuem uma taxa de casos substâncialmente menores:

| Cidade (2023) | % Pop. Impactada | Perfil Regional |
| :--- | :--- | :--- |
| **Ribeirão Pires** | 0.12% | Estância Turística / Cinturão Verde do ABC |
| **Itanhaém** | 0.07% | Litoral Sul / Baixa Carga Industrial |
| **Bertioga** | 0.01% | Estância Balneária / Preservação Ambiental |

<br>
Note que Mauá (Polo Químico Industrial) apresenta uma incidência 3x maior que sua vizinha Ribeirão Pires, apesar de compartilharem condições climáticas semelhantes.

<br>

### 2. Inconsistência de Monitoramento
A análise revelou lacunas e picos sem explicação técnica clara nos dados ambientais, sugerindo a necessidade de maior investimento em monitoramento constante. Sem dados de qualidade, não existe decisão de saúde pública de qualidade.

<br>

### 3. Modelagem Preditiva (ARIMA)
Utilizei o modelo ARIMA para projetar uma estimativa de casos de SRAG até o fim de 2026 em São Paulo. Os resultados indicam uma manutenção da média alta de casos, reforçando que, sem intervenção em políticas de emissões, o cenário de saúde tende a não apresentar melhora espontânea.

---

## Tecnologias e Fontes Utilizadas
* **Linguagem:** Python (Pandas, NumPy)
* **Análise Estatística:** Matplotlib, Statsmodels (ARIMA para séries temporais)
* **Visualização:** Plotly (Gráficos interativos de correlação e séries temporais)
* **Deploy:** Streamlit (Dashboard interativo para apresentação de insights).
* **Fontes de Dados:** DATASUS, CETESB, IBGE.

---

## Como Executar o Projeto
1. Clone este repositório: `git clone https://github.com/IIIgorMoura/analise-poluicao-saude-srag.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o Dashboard: `streamlit run analise.py`

---