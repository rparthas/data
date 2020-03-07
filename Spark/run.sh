#docker cp ~/Data/Region_Grocery spark-master:/
#docker cp ~/Data/Region_Grocery spark-worker-1:/
#docker cp ~/Data/Region_Grocery spark-worker-2:/
sbt package
docker cp target/scala-2.11/spark_2.11-0.1.jar spark-master:/
docker cp target/scala-2.11/spark_2.11-0.1.jar spark-worker-1:/
docker cp target/scala-2.11/spark_2.11-0.1.jar spark-worker-2:/
docker exec -it spark-master spark/bin/spark-submit \
  --class "com.edu.spark.Main" \
  --master spark://spark-master:7077 \
  spark_2.11-0.1.jar Region_Grocery\


