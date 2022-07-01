import unittest
import pyspark.sql.functions as F
from pyspark.sql import SparkSession


class DLTPipelineResults(unittest.TestCase):

    def test_postprocess(self):
        spark = SparkSession.builder.getOrCreate()

        # DLT pipeline silver table
        df = spark.table("cicd_lorenzo_rubio_databricks_com.sv_cleaned_new_txs")
        # check the transformation here
        self.assertEqual(
            (df
             .withColumn("total_acidity_expected", F.col("fixed_acidity") + F.col("volatile_acidity"))
             .filter(F.col("total_acidity") != F.col("total_acidity_expected"))
             .count()),
            0
        )
        # sanity
        self.assertEqual(
            df.count(),
            4074
        )
