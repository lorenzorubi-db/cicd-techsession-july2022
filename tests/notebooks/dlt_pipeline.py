# Databricks notebook source
# MAGIC %pip install /dbfs/projects/cicd-smoother/wheel/versions/cicd_project-0.0.1-py3-none-any.whl

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from app.feature_engineering import engineer_features

# COMMAND ----------

@dlt.create_table(comment="New raw clickstream data incrementally ingested from cloud object storage landing zone")
def BZ_raw_txs():
  return (
    spark.readStream.format("cloudFiles")
      .option("cloudFiles.format", "json")
      .option("cloudFiles.inferColumnTypes", "true")
      .load("/databricks-datasets/retail-org/sales_orders/"))

# COMMAND ----------

@dlt.create_table(comment="apply transformation in UAT")
def SV_cleaned_new_txs():
  txs = dlt.read_stream("BZ_raw_txs").alias("txs")
  return (
    txs
    .withColumn("fixed_acidity", F.col("number_of_line_items"))
    .withColumn("volatile_acidity", F.col("number_of_line_items"))
    .transform(engineer_features)
  )
