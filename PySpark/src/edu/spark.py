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

    def write_csv_file(self, input_file, output_file):
        file = self.spark.read.csv(input_file)
        file.write.csv(output_file)
        return self.load_csv_file(output_file)

    def write_parquet_file(self, input_file, output_file):
        file = self.spark.read.csv(input_file)
        file.write.parquet(output_file)
        file = self.spark.read.parquet(output_file)
        return file.count()

    def test_sql(self, input_file):
        file = self.spark.read.csv(input_file)
        file.write.saveAsTable("sample_csv", mode="Overwrite")
        result_df = self.spark.sql("select * from sample_csv")
        return result_df.count()
