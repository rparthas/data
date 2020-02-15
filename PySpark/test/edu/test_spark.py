import unittest
from src.edu import spark


class TestSpark(unittest.TestCase):

    def setUp(self):
        self.demo = spark.Demo()

    def test_load_text_file(self):
        count = self.demo.load_text_file("data/sampletext.txt")
        self.assertEqual(128457, count)

    def test_load_csv_file(self):
        count = self.demo.load_csv_file("data/samplecsv.csv")
        self.assertEqual(93, count)
