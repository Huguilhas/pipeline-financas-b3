import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(
    page_title="Pipeline Cotações B3",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pipeline de Cotações B3")
st.markdown("Dashboard de análise de ações da B3")

DB_PATH = "data/gold/dev.duckdb"

@st.cache_data
def carregar_dados(query: str) -> pd.DataFrame:
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute(query).df()
    conn.close()
    return df

cotacoes = carregar_dados("SELECT * FROM stage_cotacoes ORDER BY date")
retorno = carregar_dados("SELECT * FROM mart_retorno_diario ORDER BY date")
volatilidade = carregar_dados("SELECT * FROM mart_volatilidade ORDER BY volatilidade DESC")

# --- MÉTRICAS ---
st.subheader("Resumo de Volatilidade")
cols = st.columns(5)
for i, row in volatilidade.iterrows():
    cols[i].metric(
        label=row['ticker'],
        value=f"{row['retorno_medio']:.2f}%",
        delta=f"vol: {row['volatilidade']:.2f}"
    )

st.divider()

# --- FILTRO ---
tickers = cotacoes['ticker'].unique().tolist()
ticker_selecionado = st.selectbox("Selecione uma ação", tickers)

st.divider()

# --- GRÁFICO DE COTAÇÕES ---
st.subheader(f"Cotações — {ticker_selecionado}")
df_ticker = cotacoes[cotacoes['ticker'] == ticker_selecionado]
st.line_chart(df_ticker.set_index('date')['close'])

st.divider()

# --- RETORNO DIÁRIO ---
st.subheader(f"Retorno Diário — {ticker_selecionado}")
df_retorno = retorno[retorno['ticker'] == ticker_selecionado]
st.bar_chart(df_retorno.set_index('date')['retorno_pct'])

st.divider()

# --- TABELA DE VOLATILIDADE ---
st.subheader("Volatilidade por Ação")
st.dataframe(volatilidade, use_container_width=True)