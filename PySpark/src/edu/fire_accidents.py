from pyspark.sql import SparkSession
from pyspark.sql.types import *
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
    sf_fire_file = "hdfs://hadoop-master:9000/Fire_Incidents.parquet"
    spark = SparkSession.builder.appName("fire").getOrCreate()
    fire_df = spark.read.parquet(sf_fire_file)
    fire_df.write.saveAsTable("fire_incidents", format='parquet', mode='overwrite',
                              path='hdfs://hadoop-master:9000/Fire_incidents_table')

    few_fire_df = (fire_df
                   .select("Incident_Number", "Available_DtTm", "Call_Type")
                   .where(F.col("Call_Type") != 'Medical Incident'))
    few_fire_df.show(5, truncate=False)

    spark.sql("select  Incident_Number from fire_incidents where Call_Type != 'Medical Incident'").show(n=2)

    fire_df.select("CallType") \
        .where(F.col("CallType").isNotNull()) \
        .agg(F.countDistinct("CallType").alias("DistinctCallTypes")).show()

    (fire_df
     .select("CallType")
     .where(F.col("CallType").isNotNull())
     .distinct()
     .show(10, False))

    fire_ts_df = (fire_df
                  .withColumn("IncidentDate", F.to_timestamp(F.col("CallDate"), "MM/dd/yyyy"))
                  .drop("CallDate")
                  .withColumn("OnWatchDate", F.to_timestamp(F.col("WatchDate"), "MM/dd/yyyy"))
                  .drop("WatchDate")
                  )

    (fire_ts_df
     .select(F.sum("NumAlarms"))
     .show())
