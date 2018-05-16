# Docker และ hadoop3.1
## โปรแกรมที่ต้องลงก่อน docker git

## command สำหรับ start hadoop yarn
docker run -it -v $(pwd)/code:/code -v $(pwd)/file:/file -p 8088:8088 -p 9870:9870 -p 9864:9864 -p 19888:19888 -p 8042:8042 -p 8888:8888 chaluemwut/hadoop bash

## command copy file input to hdfs
hdfs dfs -copyFromLocal /file /input

## command run python
hadoop jar /code/hadoop-streaming.jar \
-file /code/mapper.py    -mapper /code/mapper.py \
-file /code/reducer.py   -reducer /code/reducer.py \
-input /input/* -output /output


## อ้างอิง
http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/