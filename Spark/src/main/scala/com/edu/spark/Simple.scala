package com.edu.spark

import org.apache.spark.sql.SparkSession

class Simple() {
  def execute(spark: SparkSession) = {

    val countBroadcast = spark.sparkContext.broadcast(1)
    val accumulator = spark.sparkContext.doubleAccumulator("sum")
    val nums = spark.sparkContext.parallelize(0 to 9999, 100)
    nums.foreach(a => accumulator.add(a + countBroadcast.value))
    println(accumulator.value)
  }
}


