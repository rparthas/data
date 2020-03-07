package com.edu.spark

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

class Grocery(path: String) {

  val conf: SparkConf = new SparkConf()
  val spark: SparkSession = SparkSession.builder().appName("Tesco").config(conf).getOrCreate()

  def calculateAverageVolume(): Unit = {
    val data = spark.read.option("header", "true").csv(path)
    val result = data.select("area_id", "volume")
    val agg_result = result.groupBy("area_id").agg(("volume", "avg"))
    agg_result.show(10)
  }
}
