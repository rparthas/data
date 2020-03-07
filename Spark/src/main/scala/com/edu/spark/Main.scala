package com.edu.spark

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object Main {

  // -Dspark.master=local[*]
  def main(args: Array[String]) {
    val conf: SparkConf = new SparkConf()
    val spark: SparkSession = SparkSession.builder().appName("Main").config(conf).getOrCreate()
    val grocery = new Grocery()
    grocery.calculateAverageVolume(spark, args(0))
//    new Simple().execute(spark)
  }
}
