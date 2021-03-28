from heapq import nlargest

from mrjob.job import MRJob
from mrjob.step import MRStep


class WordCount(MRJob):
    count = 10

    def steps(self):
        return [
            MRStep(mapper=self.mapper_map_words,
                   reducer=self.reducer_count_word),
            MRStep(reducer=self.top10_count)
        ]

    def mapper_map_words(self, _, line):
        for word in line.split(' '):
            yield word, 1

    def reducer_count_word(self, word, cnt):
        yield None, (sum(cnt), word)

    def top10_count(self, key, rating_pair):
        top_rated = nlargest(10, rating_pair)
        for word_cnt, word in top_rated:
            yield word, word_cnt


if __name__ == '__main__':
    WordCount.run()
