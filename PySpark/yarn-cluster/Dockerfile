FROM ubuntu:16.04

WORKDIR /root

# install openssh-server, openjdk and wget
RUN apt-get update && apt-get install -y openssh-server openjdk-8-jdk wget vim

# install hadoop 2.7.7
RUN wget https://mirrors.estointernet.in/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz&& \
    tar -xzvf hadoop-2.7.7.tar.gz && \
    mv hadoop-2.7.7 /usr/local/hadoop && \
    rm hadoop-2.7.7.tar.gz

# install spark
RUN wget http://apachemirror.wuchna.com/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz && \
    tar -xvf spark-2.4.7-bin-hadoop2.7.tgz && \
    mv spark-2.4.7-bin-hadoop2.7 /usr/local/spark && \
    rm spark-2.4.7-bin-hadoop2.7.tgz

RUN wget https://mirrors.estointernet.in/apache/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xvf pig-0.17.0.tar.gz && \
    mv pig-0.17.0 /usr/local/hadoop/pig && \
    rm pig-0.17.0.tar.gz

RUN wget https://mirrors.estointernet.in/apache/tez/0.9.2/apache-tez-0.9.2-bin.tar.gz && \
    tar -xvf apache-tez-0.9.2-bin.tar.gz  && \
    mkdir /usr/local/hadoop/tez && \
    mv apache-tez-0.9.2-bin /usr/local/hadoop/tez/tez && \
    rm apache-tez-0.9.2-bin.tar.gz

RUN wget https://archive.apache.org/dist/hive/hive-2.3.6/apache-hive-2.3.6-bin.tar.gz && \
    tar -xvf apache-hive-2.3.6-bin.tar.gz && \
    mv apache-hive-2.3.6-bin /usr/local/hive && \
    rm apache-hive-2.3.6-bin.tar.gz 

RUN wget http://archive.apache.org/dist/db/derby/db-derby-10.12.1.1/db-derby-10.12.1.1-bin.tar.gz && \
    tar -xvf db-derby-10.12.1.1-bin.tar.gz && \
    mv db-derby-10.12.1.1-bin /usr/local/derby && \
    rm db-derby-10.12.1.1-bin.tar.gz

RUN apt update && apt install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.1

# set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 
ENV HADOOP_HOME=/usr/local/hadoop 
ENV SPARK_HOME=/usr/local/spark
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
ENV LD_LIBRARY_PATH=/usr/local/hadoop/lib/native:$LD_LIBRARY_PATHLD_LIBRARY_PATH
ENV PIG_HOME=/usr/local/hadoop/pig
ENV HIVE_HOME=/usr/local/hive
ENV DERBY_HOME=/usr/local/derby
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PIG_HOME/bin:$HIVE_HOME/bin:$DERBY_HOME/bin
ENV CLASSPATH $CLASSPATH:/usr/local/Hadoop/lib/*:.
ENV CLASSPATH $CLASSPATH:/usr/local/hive/lib/*:.

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

RUN mkdir -p ~/hdfs/namenode && \
    mkdir -p ~/hdfs/datanode && \
    mkdir $HADOOP_HOME/logs

COPY config/* /tmp/

RUN mv /tmp/ssh_config ~/.ssh/config && \
    mv /tmp/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh && \
    mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \
    mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    mv /tmp/slaves $HADOOP_HOME/etc/hadoop/slaves && \
    mv /tmp/start-hadoop.sh ~/start-hadoop.sh && \
    mv /tmp/spark-defaults.conf $SPARK_HOME/conf/spark-defaults.conf && \
    mkdir /usr/local/hadoop/tez/conf/ && \
    mv /tmp/tez-site.xml /usr/local/hadoop/tez/conf/tez-site.xml  && \
    mv /tmp/hive-site.xml /usr/local/hive/conf/hive-site.xml && \
    cp /usr/local/hive/conf/hive-env.sh.template /usr/local/hive/conf/hive-env.sh 


RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install numpy && \
    pip install mrjob

RUN chmod +x ~/start-hadoop.sh && \
    chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh

# format namenode
RUN /usr/local/hadoop/bin/hdfs namenode -format

CMD [ "sh", "-c", "service ssh start; bash"]


