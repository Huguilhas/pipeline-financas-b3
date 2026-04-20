# Pipeline de Cotacoes B3

pipeline de dados para coleta, tratamento e analise de cotacoes da b3, seguindo a arquitetura medalion

---
![Python](https://img.shields.io/badge/python-3.11-blue)
![dbt](https://img.shields.io/badge/dbt-core-orange)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![yfinance](https://img.shields.io/badge/yfinance-1.3.0-yellow)
![Pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)
![DuckDB](https://img.shields.io/badge/duckdb-yellow?logo=duckdb&logoColor=black)
![Airflow](https://img.shields.io/badge/airflow-2.x-017CEE?logo=apacheairflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-red?logo=streamlit&logoColor=white)
![Airflow](https://img.shields.io/badge/airflow-3.1-017CEE?logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-29.x-2496ED?logo=docker&logoColor=white)

# Arquitetura
![arquitetura](docs/arquitetura.png)
- **Bronze** — dados brutos extraídos via yfinance em CSV
- **Silver** — dados limpos e tipados via dbt (stage_cotacoes)
- **Gold** — modelos analíticos via dbt (retorno diário e volatilidade)
- Orquestrado pelo **Apache Airflow** rodando em Docker.
## Estrutura
pipeline-financas-b3/  
├── source/          ← scripts de extração  
├── cotacoes_b3/     ← projeto dbt  
│   ├── models/  
│   │   ├── staging/ ← camada silver  
│   │   └── marts/   ← camada gold  
├── data/  
│   └── bronze/      ← dados brutos CSV  
└── docs/            ← diagramas e documentação  

## 🗒️Stack
- **yfinance** — coleta de cotações da B3
- **pandas** — manipulação dos dados
- **dbt + DuckDB** — transformação em camadas bronze/silver/gold
- **Apache Airflow** — orquestração e agendamento do pipeline
- **Streamlit** — visualização dos dados

## Como rodar

### Pré-requisitos
- Docker Desktop instalado e rodando
- Git instalado

### 1. Clonar o repositório
```bash
git clone https://github.com/Huguilhas/pipeline-financas-b3.git
cd pipeline-financas-b3
```

### 2. Subir o ambiente
```bash
docker compose up --build -d
```

### 3. Acessar o Airflow
- URL: http://localhost:8080
- Usuário: `admin`
- Senha: `admin`

### 4. Executar o pipeline
- Acesse a DAG `pipeline_cotacoes_b3`
- Clique em **Trigger DAG**

---

### Rodar localmente sem Docker

### 1. Criar ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Extrair dados
```bash
python source/extracao.py
```

### 3. Rodar transformações dbt
```bash
cd cotacoes_b3
dbt run
dbt test
```