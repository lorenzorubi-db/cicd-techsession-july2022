# Databricks notebook source
# uncomment the lines below if you want to run manually from an interactive cluster
# %pip install /dbfs/projects/cicd-smoother/{branch_name}/wheel/versions/cicd_project-0.0.1-py3-none-any.whl
# %pip install xmlrunner==1.7.7
# %pip install html-testRunner==1.2.1

# COMMAND ----------

import os
import pyspark.sql.functions as F
from tests.utils.test_utils import run_test_cases

# COMMAND ----------

branch_name = dbutils.widgets.get("branch_name")

# COMMAND ----------

reports_path = f"/tmp/{branch_name}/test-reports"
xml_reports_path = f"{reports_path}/xml"
html_reports_path = f"{reports_path}/html"

dbutils.fs.rm(f"{xml_reports_path}", True)
dbutils.fs.rm(f"{html_reports_path}", True)

# COMMAND ----------

run_test_cases(output_path=f"/dbfs/{xml_reports_path}")

# COMMAND ----------

from tests.utils.test_utils import output_type_enum
run_test_cases(output_path=f"/dbfs/{html_reports_path}", output_type=output_type_enum["html"])

for filename in os.listdir(f"/dbfs/{html_reports_path}"):
  with open(f"/dbfs/{html_reports_path}/{filename}", "r") as f:
    displayHTML(f.read())

# COMMAND ----------

results_df = (
    spark.read
        .format("xml")
        .option("rowTag", "testsuite")
        .load(f"{xml_reports_path}")
)

(results_df
 .withColumn("testsuite_name", F.split(F.col("_name"), "-").getItem(0))
 .withColumn("timestamp", F.to_timestamp(F.split(F.col("_name"), "-").getItem(1), "yyyyMMddHHmmss"))
 .withColumn("branch", F.lit(branch_name))
 .write
 .mode("append")
 .format("delta")
 .saveAsTable("test_results")
 )
