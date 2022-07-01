from pyspark.sql import functions as F


def engineer_features(df):
	return df.withColumn("total_acidity", F.col("fixed_acidity") + F.col("volatile_acidity"))


def rename_columns(df):
	renamed_columns = [F.col(col_name).alias(col_name.replace(" ", "_")) for col_name in df.columns]
	return df.select(renamed_columns)
