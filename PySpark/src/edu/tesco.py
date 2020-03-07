from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType

spark = SparkSession.builder. \
    appName("Tesco").getOrCreate()


def execute():
    data = spark.read.option("header", True).csv("Region_Grocery/")
    result = data.withColumn("volume", data["volume"].cast(DoubleType()))
    agg_result = result.groupBy("area_id").avg("volume")
    agg_result.show(100)


execute()
