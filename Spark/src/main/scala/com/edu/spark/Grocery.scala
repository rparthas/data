package com.edu.spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.types.DoubleType

class Grocery() {

  def calculateAverageVolume(spark: SparkSession, path: String): DataFrame = {
    val data = spark.read.option("header", "true").csv(path)
    val result = data.withColumn("volume", data("volume").cast(DoubleType)).select("area_id", "volume")
    val agg_result = result.groupBy("area_id").agg(("volume", "avg"))
    agg_result
  }

  def calculateSumOfVolumeAverages(spark: SparkSession, input: DataFrame): Double = {
    val countBroadcast = spark.sparkContext.broadcast(1)
    val accumulator = spark.sparkContext.doubleAccumulator("sum")
    input.foreach(row => accumulator.add(row.getAs[Double](1) + countBroadcast.value))
    accumulator.value
  }
}
