from mrjob.job import MRJob
from mrjob.step import MRStep


class MostPopularMovie(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer=self.reducer_sort_ratings)
        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, int(rating)

    def reducer_count_ratings(self, movie_id, rating):
        yield str(sum(rating)).zfill(5), movie_id

    def reducer_sort_ratings(self, rating, movies):
        for movie in movies:
         yield movie, rating


class RatingsBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings)
        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield rating, 1

    def reducer_count_ratings(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    # RatingsBreakdown.run()
    MostPopularMovie.run()
