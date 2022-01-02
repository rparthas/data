import sys

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("demo").getOrCreate()
df = spark.range(0, 10000, 1, 8)
print(df.rdd.getNumPartitions())

path = "../../data/"
df = spark.read.text(f"{path}/sample-2mb-text-file.txt")
df.show(10)
print(df.count())

sf_fire_file = path + "Fire_Department_Calls_for_Service.csv"
spark = SparkSession.builder.appName("fire").getOrCreate()
df = spark.read.option("header", True).csv(sf_fire_file)
df.show(10)
