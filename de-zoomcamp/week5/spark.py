from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark import SparkConf
from pyspark.sql.types import *

conf = SparkConf()
conf.set("spark.executor.memory", "8g")
conf.set("spark.driver.memory", "4g")
conf.set("spark.cores.max", "4")

spark = SparkSession.builder.master("local[4]"). \
    appName("sparkzoomcamp").config(conf=conf).getOrCreate()

print(spark.version)
