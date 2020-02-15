from pyspark.sql import SparkSession
from pyspark import SparkConf


class Demo():
    def __init__(self):
        self.spark = SparkSession.builder.master("local"). \
            appName("Demo").config(conf=SparkConf()).getOrCreate()

    def load_text_file(self, file):
        file = self.spark.read.text(file)
        file.printSchema()
        return file.count()

    def load_csv_file(self, file):
        file = self.spark.read.csv(file)
        file.printSchema()
        return file.count()
