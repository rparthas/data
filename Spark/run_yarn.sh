docker cp ~/Data/Region_Grocery hadoop-master:/root/
docker exec -it hadoop-master hadoop fs -copyFromLocal Region_Grocery/ /
sbt package
docker cp target/scala-2.11/spark_2.11-0.1.jar hadoop-master:/usr/local/spark/examples/jars/
docker exec -it hadoop-master spark-submit \
  --master yarn --deploy-mode client \
  --class "com.edu.spark.Main" \
  /usr/local/spark/examples/jars/spark_2.11-0.1.jar hdfs://hadoop-master:9000/Region_Grocery/ hdfs://hadoop-master:9000/Output/