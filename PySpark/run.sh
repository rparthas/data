## Spark Data
# docker cp ~/Data/Region_Grocery hadoop-master:/root/
# docker exec -it hadoop-master hadoop fs -copyFromLocal Region_Grocery/ /
# docker exec -it hadoop-master hadoop fs -rm -r /Output
# docker cp src/edu/tesco.py hadoop-master:/root/
# docker exec -it hadoop-master spark-submit \
# --deploy-mode cluster \
#  --num-executors 3 \
#   /root/tesco.py hdfs://hadoop-master:9000/Region_Grocery/ hdfs://hadoop-master:9000/Output/

## Jacko
#docker run -d -p 5601:5601 -p 9200:9200 --net=hadoop --name jacko1 jacko
#docker exec -i -t jacko1 python jacko/Jacko.py --history_server hadoop-master --elasticsearch localhost

## HDFS Course
# docker exec -it hadoop-master rm -rf /root/spark-warehouse/
# docker cp data/HadoopMaterials/ml-100k hadoop-master:/root/
# docker exec -it hadoop-master hadoop fs -copyFromLocal ml-100k /

# docker cp src/edu/movie_data.py hadoop-master:/root/
# docker exec -it hadoop-master python3 movie_data.py -r hadoop hdfs://hadoop-master:9000/ml-100k/u.data

#docker cp src/edu/oldgoodmovie.pig hadoop-master:/root/
#docker exec -it hadoop-master pig -x mapreduce oldgoodmovie.pig

#docker cp src/edu/mostworstmovie.pig hadoop-master:/root/
#docker exec -it hadoop-master pig -x tez mostworstmovie.pig

#docker cp src/edu/lowest_score_movie.py hadoop-master:/root/
#docker exec -it hadoop-master spark-submit lowest_score_movie.py

#docker cp src/edu/movie_reco.py hadoop-master:/root/
#docker exec -it hadoop-master spark-submit movie_reco.py

#docker exec -it hadoop-master hadoop fs -mkdir movies
#docker exec -it hadoop-master hadoop fs -cp /ml-100k/u.data movies/movie

#docker cp data/Fire_Incidents.parquet hadoop-master:/root/
#docker exec -it hadoop-master hadoop fs -copyFromLocal Fire_Incidents.parquet /
#docker cp src/edu/fire_accidents.py hadoop-master:/root/
#docker exec -it hadoop-master spark-submit --num-executors 3 fire_accidents.py







# docker cp data/text-file hadoop-master:/root/
# docker exec -it hadoop-master hadoop fs -copyFromLocal text-file /

# docker cp src/edu/word_count.py hadoop-master:/root/
# docker exec -it hadoop-master python3 word_count.py -r hadoop hdfs://hadoop-master:9000/text-file

docker cp src/edu/spark_word_count.py hadoop-master:/root/
docker exec -it hadoop-master spark-submit --num-executors 2 spark_word_count.py hdfs://hadoop-master:9000/text-file
