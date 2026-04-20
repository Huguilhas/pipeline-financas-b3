import yfinance as yf
import pandas as pd
from datetime import datetime
import os

ACOES = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA"]

def extracao(acoes: list, periodo: str = "1y") -> pd.DataFrame:
    print(f"Extraindo Dados Para: {acoes}")
    df = yf.download(acoes, period=periodo)
    
    print('Dataframe Criado')
    return df

def transformar_long_format(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    df = df.reset_index()
    df = df.melt(id_vars=['Date'], var_name='coluna', value_name='valor')
    
    df[['metrica', 'ticker']] = df['coluna'].str.rsplit('_', n=1, expand=True)
    df = df.drop(columns=['coluna'])
    
    df = df.pivot_table(
        index=['Date', 'ticker'],
        columns='metrica',
        values='valor'
    ).reset_index()
    
    df.columns.name = None
    df = df.rename(columns={'Date': 'date'})
    df.columns = [col.lower() for col in df.columns]
    
    print("Dataframe Tratado")
    
    return df

def salvar_camada_bronze(df: pd.DataFrame) -> None:
    caminho_de_saida = f"data/bronze/raw_{datetime.today().date()}.csv"
    
    os.makedirs("data/bronze", exist_ok=True)
    
    df.to_csv(caminho_de_saida, index=False)
    
    print(f"Salvando {len(df)} Registros")
    print(f"Salvo em {caminho_de_saida}")

if __name__ == "__main__":
    df_bruto = extracao(ACOES)
    df_tratado = transformar_long_format(df_bruto)
    salvar_camada_bronze(df_tratado)