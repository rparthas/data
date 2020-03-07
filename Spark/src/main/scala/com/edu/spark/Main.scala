package com.edu.spark

object Main {

  // -Dspark.master=local[*]
  def main(args: Array[String]) {
    new Grocery(args(0)).calculateAverageVolume()
  }
}
