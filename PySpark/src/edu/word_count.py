from mrjob.job import MRJob
from mrjob.step import MRStep


class WordCount(MRJob):
    count = 10

    def steps(self):
        return [
            MRStep(mapper=self.mapper_map_words,
                    reducer=self.reducer_count_word),
            MRStep(mapper=self.mapper_reverse_count,
                reducer=self.top10_count),
        ]

    def mapper_map_words(self, _, line):
        for word in line.split(' '):
            yield word, 1

    def reducer_count_word(self, word, cnt):
        yield sum(cnt),word

    def mapper_reverse_count(self, word, cnt):
        yield -1 * cnt, word

    def top10_count(self, cnt, words):
        for word in words:
            if self.count > 0:
                self.count -= 1
                yield word, -1 * cnt


if __name__ == '__main__':
    WordCount.run()
