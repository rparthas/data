package com.edu.spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.DoubleType

class Grocery() {

  def calculateAverageVolume(spark: SparkSession, path: String): Unit = {
    val data = spark.read.option("header", "true").csv(path)
    val result = data.withColumn("volume", data("volume").cast(DoubleType)).select("area_id", "volume")
    val agg_result = result.groupBy("area_id").agg(("volume", "avg"))
    agg_result.show(10)
  }
}
