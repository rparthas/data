docker cp ~/Data/Region_Grocery namenode:/
docker exec -it namenode hdfs dfs -put Region_Grocery /
#docker cp ~/git/data/PySpark/src/edu/tesco.py spark-master:/
#docker exec -it spark-master /spark/bin/spark-submit tesco.py