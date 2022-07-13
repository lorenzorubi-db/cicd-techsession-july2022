import unittest
from pyspark.sql import SparkSession
from app.feature_engineering import engineer_features, rename_columns


class FeatureEngineeringV2(unittest.TestCase):

    def test_preprocess_v2(self):
        spark = SparkSession.builder.getOrCreate()

        df = spark.createDataFrame([[2.8, 3.1], [0.0, 20.2]]).toDF("fixed acidity", "volatile acidity")
        df = df.transform(rename_columns)
        actual_df = df.transform(engineer_features) 

        expected_df = spark.createDataFrame(
            [
                [2.8, 3.1, 5.9],
                [0.0, 20.2, 20.2],
            ]
        ).toDF("fixed_acidity", "volatile_acidity", "total_acidity")

        self.assertEqual(actual_df.collect(), expected_df.collect())
