from pyspark import Row
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import lit

PATH = "hdfs://hadoop-master:9000"
rating_file = "{0}/ml-100k/u.data".format(PATH)
movie_file = "{0}/ml-100k/u.item".format(PATH)


def parse_movie_rating_row(line):
    data = line.split()
    return Row(movie_id=int(data[1]), rating=float(data[2]), user=int(data[0]))


def parse_movie(movie_line):
    movie = movie_line.split('|')
    return Row(movie_id=int(movie[0]), movie_name=movie[1])


if __name__ == "__main__":
    spark = SparkSession.builder. \
        appName("WorstMovie").getOrCreate()

    ratings_file = spark.sparkContext.textFile(rating_file)
    movie_ratings = spark.createDataFrame(ratings_file.map(parse_movie_rating_row)).cache()

    als = ALS(itemCol='movie_id')
    model = als.fit(movie_ratings)

    popular_movies = movie_ratings.groupBy('movie_id').count().filter('count > 100') \
        .select('movie_id').withColumn('user', lit(0))

    for recommendation in model.recommendForAllUsers(1).collect():
        print(recommendation)
