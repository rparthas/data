CREATE EXTERNAL TABLE IF NOT EXISTS movies(
    userID INT,
    movieID INT,
    rating INT,
    time INT
)
ROW FORMAT DELIMITED FIELDS
TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/movies';


CREATE VIEW most_rated_movies AS
select movies.movieID,avg(rating) as rating from movies ,(
select movieID,count(1) as cnt from movies group by movieID) moviecnt
where movies.movieID = moviecnt.movieID and moviecnt.cnt > 10
group by movies.movieID ;


select * from most_rated_movies order by rating desc limit 10;
select * from most_rated_movies order by rating asc limit 10;