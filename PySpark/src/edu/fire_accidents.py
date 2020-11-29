from pyspark.sql.types import *
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# Programmatic way to define a schema
fire_schema = StructType([StructField('CallNumber', IntegerType(), True),
                          StructField('UnitID', StringType(), True),
                          StructField('IncidentNumber', IntegerType(), True),
                          StructField('CallType', StringType(), True),
                          StructField('CallDate', StringType(), True),
                          StructField('WatchDate', StringType(), True),
                          StructField('CallFinalDisposition', StringType(), True),
                          StructField('AvailableDtTm', StringType(), True),
                          StructField('Address', StringType(), True),
                          StructField('City', StringType(), True),
                          StructField('Zipcode', IntegerType(), True),
                          StructField('Battalion', StringType(), True),
                          StructField('StationArea', StringType(), True),
                          StructField('Box', StringType(), True),
                          StructField('OriginalPriority', StringType(), True),
                          StructField('Priority', StringType(), True),
                          StructField('FinalPriority', IntegerType(), True),
                          StructField('ALSUnit', BooleanType(), True),
                          StructField('CallTypeGroup', StringType(), True),
                          StructField('NumAlarms', IntegerType(), True),
                          StructField('UnitType', StringType(), True),
                          StructField('UnitSequenceInCallDispatch', IntegerType(), True),
                          StructField('FirePreventionDistrict', StringType(), True),
                          StructField('SupervisorDistrict', StringType(), True),
                          StructField('Neighborhood', StringType(), True),
                          StructField('Location', StringType(), True),
                          StructField('RowID', StringType(), True),
                          StructField('Delay', FloatType(), True)])

if __name__ == '__main__':
    sf_fire_file = "hdfs://hadoop-master:9000/Fire_Incidents.csv"
    spark = SparkSession.builder.appName("fire").getOrCreate()
    fire_df = spark.read.csv(sf_fire_file, header=True, schema=fire_schema)
    # fire_df.write.format("parquet").save("hdfs://hadoop-master:9000/Fire_Incidents.parquet")
    # fire_df.write.format("parquet").saveAsTable("fire_calls")

    # few_fire_df = (fire_df
    #                .select("IncidentNumber", "AvailableDtTm", "CallType")
    #                .where("CallType != 'Medical Incident'"))
    # few_fire_df.show(5, truncate=False)
    #
    # fire_df.select("CallType") \
    #     .where(F.col("CallType").isNotNull()) \
    #     .agg(F.countDistinct("CallType").alias("DistinctCallTypes")).show()
    #
    # (fire_df
    #  .select("CallType")
    #  .where(F.col("CallType").isNotNull())
    #  .distinct()
    #  .show(10, False))

    new_fire_df = fire_df.withColumnRenamed("Delay", "ResponseDelayedinMins")
    (new_fire_df
     .select("ResponseDelayedinMins")
     .where(F.col("ResponseDelayedinMins") > 5)
     .show(5, False))

    fire_ts_df = (new_fire_df
                  .withColumn("IncidentDate", F.to_timestamp(F.col("CallDate"), "MM/dd/yyyy"))
                  .drop("CallDate")
                  .withColumn("OnWatchDate", F.to_timestamp(F.col("WatchDate"), "MM/dd/yyyy"))
                  .drop("WatchDate")
                  .withColumn("AvailableDtTS", F.to_timestamp(F.col("AvailableDtTm"),
                                                              "MM/dd/yyyy hh:mm:ss a"))
                  .drop("AvailableDtTm"))

    (fire_ts_df
     .select(F.sum("NumAlarms"), F.avg("ResponseDelayedinMins"),
             F.min("ResponseDelayedinMins"), F.max("ResponseDelayedinMins"))
     .show())
