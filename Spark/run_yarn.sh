docker cp ~/Data/Region_Grocery hadoop-master:/root/
docker exec -it hadoop-master hadoop fs -copyFromLocal Region_Grocery/ /
docker exec -it hadoop-master hadoop fs -rm -r /Output
sbt package
docker cp target/scala-2.11/spark_2.11-0.1.jar hadoop-master:/root/
docker exec -it hadoop-master spark-submit \
  --master yarn --deploy-mode cluster \
  --num-executors 3 \
  --class "com.edu.spark.Main" \
  /root/spark_2.11-0.1.jar hdfs://hadoop-master:9000/Region_Grocery/ hdfs://hadoop-master:9000/Output/