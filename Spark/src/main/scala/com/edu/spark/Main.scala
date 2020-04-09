package com.edu.spark

import org.apache.spark.{SparkConf, SparkExecutorInfo}
import org.apache.spark.sql.SparkSession

object Main {

  // -Dspark.master=local[*]
  def main(args: Array[String]) {
    val conf: SparkConf = new SparkConf()
    val spark: SparkSession = SparkSession.builder().appName("Main").config(conf).getOrCreate()
    val grocery = new Grocery()
    val result = grocery.calculateAverageVolume(spark, args(0))
    result.show(10)
    println("Sum of Avg volumes: " + grocery.calculateSumOfVolumeAverages(spark, result))
    Thread.sleep(60000)

  }
}
