ratings = LOAD 'hdfs://hadoop-master:9000/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);
metadata = LOAD 'hdfs://hadoop-master:9000/ml-100k/u.item' USING PigStorage('|')
	AS (movieID:int, movieTitle:chararray, releaseDate:chararray, videoRealese:chararray, imdblink:chararray);
   
nameLookup = FOREACH metadata GENERATE movieID, movieTitle,
	ToUnixTime(ToDate(releaseDate, 'dd-MMM-yyyy')) AS releaseTime;
   
ratingsByMovie = GROUP ratings BY movieID;
avgRatings = FOREACH ratingsByMovie GENERATE group as movieID, AVG(ratings.rating) as avgRating,COUNT(ratings.rating) as ratingCount;
oneStarMovies = FILTER avgRatings BY avgRating < 2.0;
oneStarMoviesWithData = JOIN oneStarMovies BY movieID, nameLookup BY movieID;
mostWorstMovies = FOREACH oneStarMoviesWithData GENERATE movieTitle,avgRating;
mostWorstMovies = ORDER mostWorstMovies BY avgRating;
DUMP mostWorstMovies;