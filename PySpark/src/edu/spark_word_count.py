import sys

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder. \
        appName("WordCount").getOrCreate()

    text_file = spark.sparkContext.textFile(sys.argv[1])
    result = text_file.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], ascending=False) 
        
    print(result.take(10))



