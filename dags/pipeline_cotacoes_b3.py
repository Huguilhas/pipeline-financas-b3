from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import sys

sys.path.insert(0, '/opt/airflow/source')

from extracao import extracao, transformar_long_format, salvar_camada_bronze

ACOES = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA"]

def executar_extracao():
    df_bruto = extracao(ACOES)
    df_tratado = transformar_long_format(df_bruto)
    salvar_camada_bronze(df_tratado)

with DAG(
    dag_id="pipeline_cotacoes_b3",
    schedule="0 19 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["financas", "b3"],
) as dag:

    t1 = PythonOperator(
        task_id="extrair_cotacoes",
        python_callable=executar_extracao,
    )

    t2 = BashOperator(
        task_id="transformar_dbt",
        bash_command="cd /opt/airflow/cotacoes_b3 && dbt run",
    )

    t3 = BashOperator(
        task_id="testar_qualidade",
        bash_command="cd /opt/airflow/cotacoes_b3 && dbt test",
    )

    t1 >> t2 >> t3