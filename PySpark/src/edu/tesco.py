from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
import sys

spark = SparkSession.builder. \
    appName("Tesco").getOrCreate()


def execute():
    data = spark.read.option("header", True).csv(sys.argv[1])
    result = data.withColumn("volume", data["volume"].cast(DoubleType()))
    agg_result = result.groupBy("area_id").avg("volume")
    agg_result.write.csv(sys.argv[2])


execute()
