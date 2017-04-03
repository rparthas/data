package edu.main

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD.rddToPairRDDFunctions

object WordCount {
  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("wordCount").setMaster("yarn")
    val sc = new SparkContext(conf)
    val input = sc.textFile("/input/*")
    val words = input.flatMap(line => line.split(' '))
    val count = words.map(word => (word, 1)).reduceByKey { case (x, y) => x + y }
    count.saveAsTextFile("/output/")
  }
}