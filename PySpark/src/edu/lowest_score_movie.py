from pyspark import Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg

PATH = "hdfs://hadoop-master:9000"
rating_file = "{0}/ml-100k/u.data".format(PATH)
movie_file = "{0}/ml-100k/u.item".format(PATH)


def parse_movie_rating(line):
    data = line.split()
    return int(data[1]), (float(data[2]), 1)


def parse_movie_rating_row(line):
    data = line.split()
    return Row(movie_id=int(data[1]), movie_rating=float(data[2]), rating_count=1)


def rdd_way(ratings_input):
    return ratings_input.map(parse_movie_rating).reduceByKey(
        lambda movie1, movie2: (movie1[0] + movie2[0], movie1[1] + movie2[1])).mapValues(
        lambda movie: movie[0] / movie[1]).sortBy(lambda movie: movie[1]).take(10)


def parse_movie(movie_line):
    movie = movie_line.split('|')
    return Row(movie_id=int(movie[0]), movie_name=movie[1])


def dataframe_way(ratings_input, movies_input):
    movies = spark.createDataFrame(movies_input.map(parse_movie))
    movie_ratings = spark.createDataFrame(ratings_input.map(parse_movie_rating_row))
    # movie_avg_rating = movie_ratings.groupBy("movie_id").avg("movie_rating")
    # movie_avg_rated_count = movie_ratings.groupBy("movie_id").count()
    # movie_avg_rating_count = movie_avg_rating.join(movie_avg_rated_count, 'movie_id')
    movie_avg_rating_count = movie_ratings.groupBy("movie_id").agg(count('movie_id').alias('cnt'),
                                                                   avg('movie_rating').alias('avg_rating'))
    return movie_avg_rating_count.filter('cnt > 10').join(movies, 'movie_id') \
        .select('movie_name', 'avg_rating', 'cnt').orderBy("avg_rating").take(10)


if __name__ == "__main__":
    spark = SparkSession.builder. \
        appName("WorstMovie").getOrCreate()

    ratings_file = spark.sparkContext.textFile(rating_file)
    movies_file = spark.sparkContext.textFile(movie_file)
    print(dataframe_way(ratings_file, movies_file))
    # print(rdd_way(ratings_file))
