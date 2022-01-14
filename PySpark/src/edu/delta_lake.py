import pyspark
from delta import *

if __name__ == "__main__":
    base_path = "../../data/"
    builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    (spark
     .read
     .format("parquet")
     .load(f"{base_path}loan-risks.snappy.parquet")
     .write
     .format("delta")
     .save(f"{base_path}/loans-delta"))

spark.read.format("delta").load(f"{base_path}/loans-delta").createOrReplaceTempView("loans_delta")
spark.sql("SELECT count(*) FROM loans_delta").show()
