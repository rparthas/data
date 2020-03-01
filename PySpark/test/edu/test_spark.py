import unittest
from src.edu import spark


class TestSpark(unittest.TestCase):

    def setUp(self):
        self.demo = spark.Demo()

    def test_load_text_file(self):
        count = self.demo.load_text_file("input/sampletext.txt")
        self.assertEqual(128457, count)

    def test_load_csv_file(self):
        count = self.demo.load_csv_file("input/samplecsv.csv")
        self.assertEqual(93, count)

    def test_write_csv_file(self):
        count = self.demo.write_csv_file("input/samplecsv.csv", "output/sample.csv")
        self.assertEqual(93, count)

    def test_write_parquet_file(self):
        count = self.demo.write_parquet_file("input/samplecsv.csv", "output/sample.parquet")
        self.assertEqual(93, count)

    def test_using_sql(self):
        count = self.demo.test_sql("input/samplecsv.csv")
        self.assertEqual(93, count)
