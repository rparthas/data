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

df = spark.read.csv("/users/rajagopalps/data/fhvhv_tripdata_2021-02.csv", header=True)
# df.repartition(24).write.parquet("/users/rajagopalps/data/fhv_parquet")
df.printSchema()

df.createOrReplaceTempView("fhv")
spark.sql(
    "select count(*) from fhv where to_date(pickup_datetime) = '2021-02-15' ").show(
    10)

spark.sql(
    "select pickup_datetime, MAX(cast(to_timestamp(dropoff_datetime) as LONG) - cast(to_timestamp(pickup_datetime) as LONG)) duration "
    "from fhv group by 1 order by 2 desc ").show(1)

spark.sql(
    "select dispatching_base_num,count(*) "
    "from fhv group by 1 order by 2 desc ").show(1)

spark.sql(
    "select dispatching_base_num,count(*) "
    "from fhv group by 1 order by 2 desc ").show(1)

print(spark.version)
