from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as F

if __name__ == "__main__":
    base_path = "../../data/"
    spark = SparkSession.builder. \
        appName("StreamingExample").config("spark.sql.shuffle.partitions", 10).getOrCreate()

    blog_schema = StructType([StructField("Id", IntegerType(), True),
                              StructField("First", StringType(), True),
                              StructField("Last", StringType(), True),
                              StructField("Url", StringType(), True),
                              StructField("Published", StringType(), True),
                              StructField("Hits", StringType(), True),
                              StructField("Campaigns", ArrayType(StringType()), True)
                              ])
    df = spark.readStream.format("json").schema(blog_schema).load(f"{base_path}/streaming")

    campaign_df = df.select("Id", F.explode("campaigns").alias("campaign")).withColumn("eventTime",
                                                                                       F.current_timestamp())
    result_df = campaign_df.withWatermark("eventTime", "10 seconds") \
        .groupBy("campaign", F.window("eventTime", "2 seconds")) \
        .agg(F.count("Id").alias("campaigns"))
    result_df.writeStream.format("console").option("checkpointLocation", f"{base_path}/streaming_test_checkpoint") \
        .outputMode("append").trigger(processingTime="1 second").queryName("streaming_test").start().awaitTermination()
