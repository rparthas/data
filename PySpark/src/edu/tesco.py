from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType

conf = SparkConf()
conf.setMaster("spark://spark-master:7077")
spark = SparkSession.builder. \
    appName("Tesco").config(conf=conf).getOrCreate()


def execute():
    data = spark.read.option("header", True).csv("hdfs://namenode:9000/user/root/Region_Grocery/")
    result = data.withColumn("volume", data["volume"].cast(DoubleType()))
    agg_result = result.groupBy('area_id').avg('volume')
    agg_result.show(100)


execute()
