# Cybercrime Analytics and Visualization System (CAVS)

A Big Data Analytics academic mini-project that explores Maharashtra's reported cybercrime data for 2023 using a Streamlit dashboard and an optional Hadoop/PySpark processing stage.

## Features

- KPI cards for the official 2023 statewide total and legal-group totals.
- Interactive bar chart for the most frequent detailed crime heads.
- Pie chart for the official top-level legal grouping.
- Searchable category table and CSV download.
- Optional PySpark processing script designed to read from HDFS and write processed results back to HDFS.
- Example Apache Flume configuration for the planned ingestion stage.

## Dataset

The included CSV files were prepared from the supplied NCRB *Crime in India 2023*, Table 9A.2 data for Maharashtra.

- `data/maharashtra_cybercrime_2023_clean.csv`: detailed crime-head rows and reported case counts.
- `data/maharashtra_cybercrime_2023_summary.csv`: official high-level totals.
- Official Maharashtra total in the supplied table: **8,103 reported cybercrime cases in 2023**.

### Important interpretation note

The detailed crime-head rows and high-level legal-group totals represent different levels of the source table. Do not sum every detailed row and assume it must equal 8,103. This project uses 2023 data only; it does not claim year-wise trends or district-level analysis.

## Run the dashboard locally

Requires Python 3.10 or newer.

### Windows (PowerShell)

```powershell
cd CAVS_Maharashtra_Cybercrime
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can install and run without activating the environment:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

### Linux / Ubuntu

```bash
cd CAVS_Maharashtra_Cybercrime
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard runs locally and does not require Hadoop to be running.

## Optional Hadoop + PySpark stage

The included `process_data.py` expects the detailed CSV to be available at:

`hdfs://localhost:9000/cybercrime/maharashtra/maharashtra_cybercrime_2023_clean.csv`

After HDFS is running, upload the file:

```bash
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /cybercrime/maharashtra
$HADOOP_HOME/bin/hdfs dfs -put -f data/maharashtra_cybercrime_2023_clean.csv /cybercrime/maharashtra/
```

Run the PySpark script in an environment where PySpark can connect to your HDFS:

```bash
python3 process_data.py
```

The script writes processed CSV part files to:

`hdfs://localhost:9000/cybercrime/processed/maharashtra_2023_categories`

## Flume ingestion configuration

An example configuration is included at `flume/cybercrime.conf`. It describes a spool-directory source and HDFS sink. Flume/Hadoop compatibility can vary by version, so test this configuration in the target environment before describing the live Flume-to-HDFS ingestion as verified.

## Project pipeline

**Dataset → (Flume ingestion stage) → HDFS → PySpark cleaning/processing → Streamlit + Plotly visualization**

The Streamlit dashboard is independently runnable for convenient review. The Flume and HDFS steps are documented separately because they require a correctly configured Hadoop/Flume environment.

## Technology stack

- Python
- Pandas
- Streamlit
- Plotly
- Apache Hadoop HDFS (optional processing pipeline)
- Apache PySpark (optional processing pipeline)
- Apache Flume (example ingestion configuration)

## Academic scope and limitations

This is a descriptive analysis of reported cases in Maharashtra for 2023. It is not a prediction system, does not infer causation, and does not contain district-level or multi-year data. Crime-head labels are retained from the source data for traceability.
