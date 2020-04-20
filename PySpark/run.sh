docker cp ~/Data/Region_Grocery hadoop-master:/root/
docker exec -it hadoop-master hadoop fs -copyFromLocal Region_Grocery/ /
docker exec -it hadoop-master hadoop fs -rm -r /Output
docker cp src/edu/tesco.py hadoop-master:/root/
docker exec -it hadoop-master spark-submit \
 --deploy-mode cluster \
  --num-executors 3 \
   /root/tesco.py hdfs://hadoop-master:9000/Region_Grocery/ hdfs://hadoop-master:9000/Output/