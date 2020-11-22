## Spark Data
# docker cp ~/Data/Region_Grocery hadoop-master:/root/
# docker exec -it hadoop-master hadoop fs -copyFromLocal Region_Grocery/ /
# docker exec -it hadoop-master hadoop fs -rm -r /Output
# docker cp src/edu/tesco.py hadoop-master:/root/
# docker exec -it hadoop-master spark-submit \
# --deploy-mode cluster \
#  --num-executors 3 \
#   /root/tesco.py hdfs://hadoop-master:9000/Region_Grocery/ hdfs://hadoop-master:9000/Output/

## HDFS Course
#docker exec -it hadoop-master wget https://bootstrap.pypa.io/get-pip.py
#docker exec -it hadoop-master python get-pip.py
#docker exec -it hadoop-master pip install numpy
#docker exec -it hadoop-master pip install mrjob

#docker cp ~/Downloads/HadoopMaterials/ml-100k hadoop-master:/root/
#docker exec -it hadoop-master hadoop fs -copyFromLocal ml-100k /

# docker cp src/edu/movie_data.py hadoop-master:/root/
# docker exec -it hadoop-master python movie_data.py -r hadoop hdfs://hadoop-master:9000/ml-100k/u.data

# docker cp src/edu/oldgoodmovie.pig hadoop-master:/root/
# docker exec -it hadoop-master pig -x mapreduce oldgoodmovie.pig

#docker cp src/edu/mostworstmovie.pig hadoop-master:/root/
#docker exec -it hadoop-master pig -x tez mostworstmovie.pig

#docker cp src/edu/lowest_score_movie.py hadoop-master:/root/
#docker exec -it hadoop-master spark-submit lowest_score_movie.py

docker cp src/edu/movie_reco.py hadoop-master:/root/
docker exec -it hadoop-master spark-submit movie_reco.py