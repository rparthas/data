docker cp ~/Data/Region_Grocery spark-master:/
docker cp ~/Data/Region_Grocery spark-worker-1:/
docker cp ~/Data/Region_Grocery spark-worker-2:/
docker cp ~/git/data/PySpark/src/edu/tesco.py spark-master:/
docker exec -it spark-master /spark/bin/spark-submit --master spark://spark-master:7077 tesco.py