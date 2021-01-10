#!/bin/bash
sh stop.sh

docker network create --driver=bridge hadoop

N=${1:-4}

# start hadoop master container
echo "start hadoop-master container..."
docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 8088:8088 \
                -p 7077:7077 \
                -p 16010:16010 \
                -p 18080:18080 \
                -p 4040:4040 \
                -p 8000:8000 \
                -p 8001:8001 \
                --name hadoop-master \
                --hostname hadoop-master \
                spark-hadoop:latest &> /dev/null


# start hadoop slave container
i=1
while [ $i -lt $N ]
do
	echo "start hadoop-slave$i container..."
	port=$(( 8040 + $i ))
	docker run -itd \
			-p $port:8042 \
	                --net=hadoop \
	                --name hadoop-slave$i \
	                --hostname hadoop-slave$i \
	                spark-hadoop:latest &> /dev/null
	i=$(( $i + 1 ))
done 

docker exec -it hadoop-master /root/start-hadoop.sh

docker exec -it hadoop-master hadoop fs -mkdir /spark-logs
docker exec -it hadoop-master /usr/local/spark/sbin/start-history-server.sh

docker exec -it hadoop-master hadoop fs -mkdir /tez 
docker exec -it hadoop-master hadoop fs -copyFromLocal /usr/local/hadoop/tez/tez/share/tez.tar.gz /tez/

docker exec -it hadoop-master schematool -initSchema -dbType derby

docker exec -it hadoop-master /usr/local/hbase/bin/start-hbase.sh
docker exec -it hadoop-master /usr/local/hbase/bin/hbase-daemon.sh start rest -p 8000 --infoport 8001