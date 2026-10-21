"""
Optional PySpark processing stage for the CAVS project.

Run after installing PySpark and configuring HDFS. This script reads the
cleaned detailed crime-head CSV, validates the columns, removes blank labels,
sorts reported case counts, and writes a processed CSV directory to HDFS.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim

HDFS_INPUT = "hdfs://localhost:9000/cybercrime/maharashtra/maharashtra_cybercrime_2023_clean.csv"
HDFS_OUTPUT = "hdfs://localhost:9000/cybercrime/processed/maharashtra_2023_categories"

spark = SparkSession.builder.appName("CAVS_MaharashtraCrimeAnalytics").getOrCreate()

df = (spark.read.option("header", True).option("inferSchema", True).csv(HDFS_INPUT))
required = {"Crime Category", "Cases"}
missing = required.difference(set(df.columns))
if missing:
    raise ValueError(f"Input CSV is missing expected columns: {sorted(missing)}")

processed = (
    df.select(trim(col("Crime Category")).alias("Crime Category"), col("Cases").cast("long").alias("Cases"))
      .filter(col("Crime Category").isNotNull() & (col("Crime Category") != "") & col("Cases").isNotNull())
      .filter(col("Cases") >= 0)
      .orderBy(col("Cases").desc())
)

processed.show(10, truncate=False)
(processed.coalesce(1).write.mode("overwrite").option("header", True).csv(HDFS_OUTPUT))
print(f"Processed data written to: {HDFS_OUTPUT}")
spark.stop()
